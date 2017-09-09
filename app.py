"""PDF-fill for heating cables."""
# pylama:ignore=W0512

import os
import sys
import re
import base64

from config import configure_app
from addresses.address_pymongo import (
    # get_post_area_for_post_code,
    get_address_from_street_name,
    # get_post_code_for_post_area,
    # get_location_from_address
)
from pdf_filler.helpers import (id_generator)
from models import (
    db,
    MyJSONEncoder
)
from models_product import (

    Manufacturor,
    Product,
)
from models_credentials import (
    User,
    OAuth,
    Invite,
    Customer,
    InviteType,
    Address,
    Company,
    UserRole,
    RoomItem,
    RoomTypeInfo,
    Room,
)

from my_exceptions import LocationException

from flask import (
    Flask,
    request,
    flash,
    session,
    redirect,
    render_template,
    send_from_directory,
    url_for
)
from flask.json import jsonify
import forms
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress

from sqlalchemy.orm.exc import NoResultFound
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.backend.sqla import (
    SQLAlchemyBackend
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user
)
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import wtforms_json
from flask_wtf.csrf import CSRFProtect, CSRFError
# import schemas
from form_handler import FormHandler
import my_exceptions

wtforms_json.init()


app = Flask(__name__, instance_relative_config=True)
app.json_encoder = MyJSONEncoder
configure_app(app)
Compress(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


db.init_app(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2000 per day", "500 per hour"]
)
blueprint = make_google_blueprint(
    client_id=app.config['G_CLIENT_ID'],
    client_secret=app.config['G_CLIENT_SECRET'],
    offline=True,
    scope=["profile", "email"],
    reprompt_consent=True,
)
app.register_blueprint(blueprint, url_prefix="/login")

# setup login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# setup SQLAlchemy backend
blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)
csrf = CSRFProtect(app)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    print('csrf-error: {}'.format(e))
    # TODO: Needs to actually send the json
    return jsonify({'errors': [str(e)]})


@app.errorhandler(my_exceptions.MyBaseException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.context_processor
def include_user_roles():
    return {'UserRole': UserRole}


@app.before_request
def make_session_permanent():
    """Keep sessions alive after closing browser."""
    session.permanent = True  # Default 31 days


@login_manager.user_loader
def load_user(user_id):
    """Return user by user_id."""
    return User.query.get(int(user_id))


@app.route("/login")
def login():
    """Login."""
    next_redirect = request.args.get('next')
    session['next'] = next_redirect
    if not google.authorized:
        return redirect(
            url_for("google.login",
                    redirect_url=next_redirect or url_for('view_form')))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])


@oauth_authorized.connect
def logged_in(blueprint_, token):
    """User logged in."""
    next_redirect = session.get('next')
    return redirect(next_redirect or url_for('view_form'))


@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):  # noqa
    """Create/login local user on successful OAuth login."""
    if not token:
        flash(
            "Feil: Kunne ikke logge på med {name}".format(name=blueprint.name))
        return
    # figure out who the user is
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if resp.ok:
        family_name = resp.json()["family_name"]
        given_name = resp.json()["given_name"]
        email = resp.json()["email"]
        query = User.query.filter_by(email=email)
        try:
            user = query.one()
        except NoResultFound:
            # create a user
            user = User(
                family_name=family_name,
                given_name=given_name,
                email=email,
            )
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash("Vellykket pålogging gjennom Google")
    else:
        msg = "Feil: Kunne ikke hente bruker-info fra {name}".format(
            name=blueprint.name)
        flash(msg, category="error")


@app.route("/logout")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("Du er nå logget ut")
    return redirect(url_for("view_form"))


@app.route("/cp/")
@login_required
def control_panel():
    """Control-Panel."""
    form = forms.Invite()
    signature = None
    if current_user.signature:
        signature = base64.b64encode(
            current_user.signature).decode(encoding='UTF-8')
    return render_template(
        'control-panel.html', signature=signature, form=form)


@app.route("/cp/company/")
@login_required
def control_panel_company():
    """Control-Panel for viewing users company."""
    if not current_user.company:
        flash('Du er ikke medlem av et firma enda.', 'error')
        return redirect(url_for('control_panel'))
    form = forms.Invite()
    memmbers = User.query.filter(
        User.company == current_user.company
    )
    return render_template(
        'control-panel-company.html', memmbers=memmbers, form=form)


@app.errorhandler(429)
def ratelimit_handler(e):
    """Errorhandler for ratelimiting."""
    return jsonify(
        error_message=(
            "Ta det med ro, vennligst ikke hamre i vei på serveren. "
            "Du har nådd grensen for maks antall innsendinger: {}"
        ).format(e.description),
        status=429
    )


def user_file_path(filename=None, create_random_dir=False):
    """Return full path to user-dir, with a random generated unique folder."""
    paths = [app.root_path, app.config['USER_FILES']]
    new_path = paths.copy()
    if create_random_dir:
        while os.path.exists(os.path.join(*new_path)):
            new_path = paths.copy()
            new_path.append(id_generator())
        os.mkdir(os.path.join(*new_path))
    if filename:
        new_path.append(filename)
    return os.path.join(*new_path)


def set_fields_from_product(dictionary, product, specs=None):
    """Set multiple fields from a Product-table."""
    dictionary["Betegnelse"] = product.product_type.name

    dictionary.update(product.specs)

    return dictionary


@app.route('/invite/<invite_id>', methods=['GET', 'POST'])
@app.route('/invite/')
@login_required
def get_invite(invite_id):
    """Route for getting an invite."""
    invite = Invite.get_invite_from_id(invite_id)
    if not invite:
        flash('Denne invitasjonsnøkkelen er ikke gyldig.')
        return redirect(url_for('control_panel'))
    if invite.type == InviteType.create_company:
        return set_company(invite=invite)
    elif invite.type == InviteType.company:
        pass
    if request.method == 'GET':
        return render_template('invite.html', invite=invite)

    if request.method == 'POST' and invite:
        if invite.type == InviteType.company:
            invite.invitee = current_user
            current_user.company = invite.company
            return render_template(
                'invite.html', invite=invite, newly_invite=True)


@app.route('/company/edit', methods=['GET', 'POST'])
@login_required
def set_company(invite=None):
    """Description."""
    form = forms.CreateCompany()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                current_user.company = Company.update_or_create_all(
                form,
                current_user.company)
                db.session.add(current_user)
                db.session.commit()
            except (LocationException, my_exceptions.DuplicateCompany) as e:
                flash(e.message, 'error')
                return render_template(
                    'create_company.html', invite=invite, form=form)
            if invite:
                invite.invitee = current_user
                db.session.add(invite)
                db.session.commit()
            return redirect(url_for('control_panel_company'))
        return render_template('create_company.html', invite=invite, form=form, mode='edit')
    if current_user.company:
        form.name.data = current_user.company.name
        form.org_nr.data = current_user.company.orgnumber
        form.description.data = current_user.company.description
        # TODO: contact needs fix
        form.contact_name.data = current_user.company.contacts[
            0].contact.description
        form.email.data = current_user.company.contacts[0].contact.value
        form.address.address1.data = current_user.company.address.address1
        form.address.address2.data = current_user.company.address.address2
        form.address.post_area.data = current_user.company.address.post_area
        form.address.post_code.data = current_user.company.address.post_code
        form.lat.data = current_user.company.lat
        form.lng.data = current_user.company.lng

    return render_template('create_company.html', invite=invite, form=form)


@app.route('/set_sign', methods=['POST'])
@login_required
def save_image():
    """Save an image from a data-string."""
    image_b64 = request.json.get('imageBase64')
    if not image_b64:
        raise my_exceptions.MyBaseException(
            message='Mottok ikke bildedata.',
            status_code=403,
            defcon_level=my_exceptions.DefconLevel.danger
        )
    if len(image_b64) > 200000:
        raise my_exceptions.MyBaseException(
            message='Bildedataen var for stor.',
            status_code=403,
            defcon_level=my_exceptions.DefconLevel.warning
        )
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)
    imgdata = base64.b64decode(image_data)
    if current_user.is_authenticated:
        current_user.signature = imgdata
        db.session.commit()
    return jsonify({})


@app.route('/user_files/<path:filename>', methods=['GET'])
@login_required
def download(filename):
    """Serve a file for downloading."""
    # TODO: Make sure filename is valid. (bad input)
    directory = os.path.join(app.root_path, app.config['USER_FILES'])
    return send_from_directory(directory=directory, filename=filename)


@limiter.limit("5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
@login_required
@app.route('/invite.json', methods=['GET', 'POST'])
def json_invite():
    """Return all invites from current user, or create a new one."""
    form = forms.Invite()
    if form.validate_on_submit():
        try:
            invite = Invite.create(current_user)
            db.session.add(invite)
            db.session.commit()
        except ValueError as e:
            return "{}".format(e), 403
    invites = Invite.get_invites_from_user(current_user).all()
    serialized = ([i.serialize for i in invites])
    return jsonify({
        'invites': serialized,
        'base_url': url_for('get_invite')
    })


@app.route('/json/v1/static/')
# @limiter.limit("1/second", error_message='Èn per sekund')
@limiter.limit("5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
def json_static_data():
    """Return a json-object of all products and room-type-info."""
    manufacturors = Manufacturor.query.filter(Manufacturor.name !='Thermofloor').all()
    room_types = RoomTypeInfo.query.all()
    return jsonify(
        {
            'products': [i.serialize for i in manufacturors],
            'room_type_info': [i.serialize for i in room_types]
        }
    )


@app.route('/forms.json')
# @limiter.limit("1/second", error_message='Èn per sekund')
@limiter.limit("5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
@login_required
def json_user_forms():
    """Return a json-object of all the users forms."""
    result = {
        'user_forms': [],
        'company_forms': []
    }
    page = request.args.get('page', 1)
    user_forms, user_pages = current_user.\
        get_forms(page=page)
    if current_user and current_user.company:
        company_forms, company_pages = current_user\
            .company\
            .get_forms(
                user=current_user,
                page=page
            )
        if company_forms:
            result['company_forms'] = [i.serialize(
                current_user) for i in company_forms]
            result['company_pages'] = company_pages
    if user_forms:
        result['user_forms'] = [i.serialize(current_user) for i in user_forms]
        result['user_pages'] = user_pages
    return jsonify(result)


def create_form(room_item_modification):
    """Create forms, and return a json-object with the url."""
    path = user_file_path(
        filename=(
            room_item_modification.room_item.room.customer.address.
            address1 + '.pdf'
        ),
        create_random_dir=True
    )
    form_handler = FormHandler(room_item_modification, current_user, path)
    form_handler.create()
    return jsonify({'file_download': form_handler.url})


@app.route('/json/v1/heat/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def json_heating_cable():
    """Handle a heatining-cable-form."""
    room_item = None
    room_item_id = request.args.get('id') or request.json.get('id')
    if room_item_id:
        room_item = RoomItem.by_id(room_item_id, current_user)
    if not room_item and request.method != 'POST':
        return jsonify(
            {
                'error': f'did not recieve an id {room_item_id}'})

    if request.method == 'GET':
        return create_form(room_item.latest)

    if request.method == 'DELETE':
        room_item.put_in_archive(current_user)
        return jsonify({'status': 'OK'})

    form = forms.HeatingCableForm.from_json(
        request.json, skip_unknown_keys=False)
    if not form.validate_on_submit():
        print(form.errors)
        return jsonify({'error': form.errors}), 403
    if request.method == 'GET':
        return jsonify({'url': 'aweseome.com'})
    # TODO: This is really bad. Remove the code below.
    product_id = form.product_id.data
    room_id = form.room_id.data
    product = Product.by_id(product_id)
    room = Room.by_id(room_id, current_user)
    if not product:
        raise my_exceptions.NotAProduct
    if not room:
        raise my_exceptions.NotARoom

    room_item = RoomItem.update_or_create(
        room_item=room_item,
        user=current_user,
        product_id=product_id,
        room=room,
        specs=form.specs.data,
    )
    db.session.commit()
    return jsonify(room_item.serialize)


@app.route('/json/v1/room/',
           methods=['POST', 'PUT', 'DELETE'])
@login_required
def json_room():
    """Handle a room-object"""
    form = forms.RoomForm.from_json(request.json)
    customer_id = (form.customer_id.data)
    room_id = form.id.data or request.args.get('id')
    customer = None
    room = None
    if room_id:
        room = Room.by_id(
            room_id,
            current_user)
    if not room and request.method != 'POST':
        raise my_exceptions.NotARoom
    if request.method == 'DELETE':
        room.put_in_archive(current_user)
        return jsonify({'status': 'OK'})
    if customer_id:
        customer = Customer.by_id(
            customer_id,
            current_user)
    if not customer:
        raise my_exceptions.NotACustomer()
    if not form.validate_on_submit():
        print(form.errors)
        return jsonify(form.errors), 403
    if request.method == 'POST':
        room = Room()
        db.session.add(room)
    room.update_entity({
        'name': form.room_name.data,
        'customer': customer,
        'outside': form.outside.data,
        'area': float(form.area.data),
        'heated_area': float(form.heated_area.data),
        'maxEffect': float(form.maxEffect.data),
        'normalEffect': float(form.normalEffect.data),
        'earthed_cable_screen': form.check_earthed.cable_screen.data,
        'earthed_chicken_wire': form.check_earthed.chicken_wire.data,
        'earthed_other': form.check_earthed.other.data,
        'max_temp_planning': form.check_max_temp.planning.data,
        'max_temp_installation': form.check_max_temp.installation.data,
        'max_temp_other': form.check_max_temp.other.data,
        'control_system_floor_sensor': form.check_control_system.floor_sensor.data,  # noqa
        'control_system_room_sensor': form.check_control_system.room_sensor.data,  # noqa
        'control_system_designation': form.check_control_system.designation.data,  # noqa
        'control_system_other': form.check_control_system.other.data,

    })
    db.session.commit()
    return jsonify(room.serialize)


@app.route('/json/v1/customer/',
           methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def json_customer():
    """Handle a customer-object"""
    form = forms.CustomerForm.from_json(request.json)
    customer_id = form.id.data or request.args.get('id')
    customer=None
    if customer_id:
        customer = Customer.by_id(
            customer_id,
            current_user)

    if request.method == "GET":
        if not customer_id:
            customer = current_user.last_edit
        if not customer:
            raise my_exceptions.NotACustomer()
        return jsonify(customer.serialize)

    if not customer and request.method != 'POST':
        raise my_exceptions.NotACustomer()
    if request.method == 'DELETE':
        customer.put_in_archive(current_user)

    if not form.validate_on_submit():
        print(form.errors)
        return 'incorrect data', 403
    customer = Customer.update_or_create(customer, form, current_user)
    if customer:
        return jsonify({'id': customer.id})
    raise my_exceptions.NotACustomer


@app.route('/app')
def view_form():
    """View for home."""
    # TODO: NEVER PUT THIS IN PRODUCTION!
    # login_user(User.query.filter(User.id==1).first())
    # Set up some defaults. (retrieve this from the user-config later.)
    heatingForm = forms.HeatingCableForm()
    customerForm = forms.CustomerForm()
    form = forms.CustomerForm()
    roomForm = forms.RoomForm()
    return render_template(
        'main.html',
        heatingForm=heatingForm,
        customerForm=customerForm,
        form=form,
        roomForm=roomForm
    )


@app.route('/')
def landing_page():
    """Landing-page-view."""
    return render_template("landing.html")

@login_required
@limiter.limit("200/minute", error_message='200 per minutt')
@app.route('/address/')
def search_address():
    """Search a partial address (near user)."""
    kwargs = {}
    if current_user.company:
        if current_user.company.lat and current_user.company.lng:
            kwargs['near_geo'] = [
                float(current_user.company.lat),
                float(current_user.company.lng)
            ]
        else:
            kwargs['near_post_code'] = current_user.company.address.post_code
    # Make sure 'post_code' is an int.
    try:
        post_code = request.args.get('p')
        if post_code:
            kwargs['near_post_code'] = int(post_code)
    except ValueError:
        pass
    kwargs['street_name'] = request.args.get('q')
    # Try to get a valid address from search-query
    try:
        results = get_address_from_street_name(**kwargs)
    except ValueError:
        return jsonify(None)
    formated_result = []
    for result in results:
        formated_result.append({
            'post_area': result['post_area'],
            'post_code': result['post_code'],
            'street_name': result['street_name'],
        })
    return jsonify(formated_result)


# hook up extensions to app
if __name__ == "__main__":
    if 'db' in sys.argv:
        manager.run()
    else:
        if app.config['DEBUG'] is True:
            app.run(host='0.0.0.0', port=app.config['PORT'])
