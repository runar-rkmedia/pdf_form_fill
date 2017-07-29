"""PDF-fill for heating cables."""
# pylama:ignore=W0512

import os
import sys
import decimal
import re
import base64

from config import configure_app
from datetime import datetime
from addresses.address_pymongo import (
    # get_post_area_for_post_code,
    get_address_from_street_name,
    # get_post_code_for_post_area,
    get_location_from_address
)
from field_dicts.helpers import (commafloat, id_generator)
from models import (
    db,
    Manufacturor,
    Product,
    User,
    OAuth,
    Invite,
    FilledFormModified,
    Room,
    Customer,
    InviteType,
    Address,
    Company,
    ContactType,
    UserRole
)
from vk_objects import FormField

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
from flask.json import jsonify, JSONEncoder
import forms
from flask_scss import Scss
from flask_assets import Environment, Bundle
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


class MyJSONEncoder(JSONEncoder):
    """Redefine flasks json-encoded to convert Decimals.."""

    def default(self, obj):  # noqa
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(MyJSONEncoder, self).default(obj)


app = Flask(__name__, instance_relative_config=True)
app.json_encoder = MyJSONEncoder
configure_app(app)
Compress(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


assets = Environment(app)
# js_main = Bundle(
#     # 'js/ext/knockout.validation.js',
#     # 'js/ext/nb-NO.js',
#     'js/main.js',
#     # filters='jsmin',
#     output='gen/packed.js')
# assets.register('js_main', js_main)

css = Bundle(
    # 'css/bootstrap.min.css',
    'css/style.css',
    'css/ko-bootstrap-typeahead.css',
    filters='cssmin',
    output='css/min.css'
)
assets.register('css_all', css)

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
    signature = None
    if current_user.signature:
        signature = base64.b64encode(
            current_user.signature).decode(encoding='UTF-8')
    return render_template('control-panel.html', signature=signature)


@app.route("/cp/company/")
@login_required
def control_panel_company():
    """Control-Panel for viewing users company."""
    memmbers = User.query.filter(
        User.company == current_user.company
    )
    return render_template('control-panel-company.html', memmbers=memmbers)


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
    print(dictionary)
    print('dsssssssss')

    return dictionary


def validate_fields(request_form):
    """Validate the input from a form."""
    error_fields = []
    required_fields = {
        'strings': [
            'anleggs_adresse',
            'rom_navn',
        ],
        'digits': [
            'product_id',
            'oppvarmet_areal',
        ]}
    for key in required_fields['strings']:
        field = request_form.get(key)
        if not field:
            error_fields.append(key)
    for key in required_fields['digits']:
        field = request_form.get(key)
        if not field:
            error_fields.append(key)
        else:
            try:
                commafloat(field)
            except ValueError:
                error_fields.append(key)
    return error_fields


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
        return invite_create_company(invite)
    elif invite.type == InviteType.company:
        pass
    if request.method == 'GET':
        return render_template('invite.html', invite=invite)

    if request.method == 'POST' and invite:
        if invite.type == InviteType.company:
            invite.invitee = current_user
            current_user.company = invite.company
            db.session.commit()
            return render_template(
                'invite.html', invite=invite, newly_invite=True)


def invite_create_company(invite):
    """Handle invites for creating a company."""
    form = CreateCompany()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                current_user.company = Company.update_or_create_all(form)
            except LocationException as e:
                flash(e, 'error')
                return render_template(
                    'create_company.html', invite=invite, form=form)
            if current_user.role == UserRole.user:
                current_user.role = UserRole.companyAdmin
            invite.invitee = current_user
            db.session.commit()
            flash("Firmaet '{}' ble opprettet."
                  .format(current_user.company.name))
            return redirect(url_for('control_panel_company'))
    return render_template('create_company.html', invite=invite, form=form)


@app.route('/company/<company_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_company(company_id=None, invite=None):
    """Description."""
    form = CreateCompany()
    company = Company.query.filter_by(id=company_id).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                current_user.company = Company.update_or_create_all(
                    form,
                    company)
            except LocationException as e:
                flash(e, 'error')
                return render_template(
                    'create_company.html', invite=invite, form=form)
            db.session.commit()
            return redirect(url_for('control_panel_company'))
        return render_template('create_company.html', invite=invite, form=form)

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

    return render_template('create_company.html', invite=invite, form=form)


@app.route('/set_sign', methods=['POST'])
@login_required
def save_image():
    """Save an image from a data-string."""
    image_b64 = request.values['imageBase64']
    if len(image_b64) < 200000:
        image_data = re.sub('^data:image/.+;base64,', '', image_b64)
        imgdata = base64.b64decode(image_data)
        if current_user.is_authenticated:
            current_user.signature = imgdata
            db.session.commit()
        return jsonify({'status': 200})
    return jsonify({
        'status': 403,
        'errormsg': 'Feil: Mottok en signatur-fil som var større enn antatt.'
    })


@app.route('/user_files/<path:filename>', methods=['GET'])
@login_required
def download(filename):
    """Serve a file for downloading."""
    # TODO: Make sure filename is valid. (bad input)
    directory = os.path.join(app.root_path, app.config['USER_FILES'])
    return send_from_directory(directory=directory, filename=filename)


@limiter.limit("5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
@app.route('/invite.json', methods=['GET', 'POST'])
def json_invite():
    """Return all invites from current user, or create a new one."""
    if request.method == 'POST':
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


@app.route('/products.json')
# @limiter.limit("1/second", error_message='Èn per sekund')
@limiter.limit("5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
def json_products():
    """Return a json-object of all products."""
    manufacturors = Manufacturor.query.all()

    return jsonify([i.serialize for i in manufacturors])


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


@app.route('/json/v0/customer/', methods=['POST'])
@login_required
def json_create_customer():
    """Create  customer-object"""
    form = forms.AddressForm
    if request.method == 'POST':
        result = {}
        # result['customer'] = customer.serialize
        return jsonify(result)


@app.route('/json/v1/customer/',
           methods=[
               'GET',
               'POST',
               'PUT',
               'DELETE'
           ])
@login_required
def json_edit_customer():
    """Edit a customer-object"""
    form = forms.CustomerForm(request.form)
    if not form.validate_on_submit():
        return 'incorrect data', 403
    if request.method == 'POST':
        address = Address(
            address1=form.address.address1.data,
            address2=form.address.address2.data,
            post_code=form.address.post_code.data,
            post_area=form.address.post_area.data,
        )
        customer = Customer(
            name=form.customer_name.data,
            address=address,
            company=current_user.company
        )
        db.session.add(address)
        db.session.add(customer)
        db.session.commit()
    else:
        customer = Customer.by_id(form.customer_id.data, current_user)
        if request.method == 'PUT':
            customer.address.address1 = form.address.address1.data
            customer.address.address2 = form.address.address2.data
            customer.address.post_code = form.address.post_code.data
            customer.address.post_area = form.address.post_area.data
            customer.name = form.customer_name.data
            db.session.commit()
    if customer:
        return jsonify({'customer_id': customer.id})
    return jsonify({})


@app.route('/json/v1/room/<room_id>', methods=['GET', 'DELETE'])
@login_required
def json_form(room_id):
    """Return a json-object of a form."""
    room = Room.by_id(current_user, room_id)
    if request.method == 'GET':
        if room:
            result = {}
            result['room'] = room.serialize
            return jsonify(result)
        return jsonify({})


@app.route('/json/form_mod/<filled_form_modified_id>',
           methods=['GET', 'DELETE'])
@login_required
def json_form_modification(filled_form_modified_id):
    """Return a json-object of a form-modfication."""
    form = FilledFormModified.by_id(current_user, filled_form_modified_id)
    if request.method == 'GET':
        if form:
            result = {}
            result['form'] = form.serialize
            return jsonify(result)
        return jsonify({})
    elif request.method == 'DELETE':
        form.archive_this(current_user)
        return 'deleted'


def create_form(manufacturor, dictionary=None,
                request_form=None, form_data=None, user=current_user):
    """Create a form."""
    form = FormField(manufacturor)
    if form_data:
        form.fields = form_data
    elif dictionary:
        form.set_fields_from_dict(dictionary)

    filename = request_form.get('anleggs_adresse', 'output') + '.pdf'
    output_dir = user_file_path(create_random_dir=True)
    output_pdf = os.path.join(output_dir, filename)
    dictionary = form.create_filled_pdf(output_pdf)
    stamp_with_user(user, output_pdf, form)
    return output_pdf, dictionary, form


def stamp_with_user(user, output_pdf, form):
    """Description."""
    if user.signature:
        image = os.path.join(os.path.split(output_pdf)[0], 'sign.png')
        with open(image, 'wb') as f:
            f.write(user.signature)
        stamped_pdf = form.stamp_with_image(output_pdf, image, 20, 10)
        os.remove(image)
        os.remove(output_pdf)
        os.rename(stamped_pdf, output_pdf)


def add_company_info_to_dictionary(dictionary, company):
    """Description."""
    dictionary['firma_navn'] = current_user.company.name
    dictionary['firma_orgnr'] = current_user.company.orgnumber
    dictionary['firma_adresse1'] = current_user.company.address.address1
    dictionary['firma_adresse2'] = current_user.company.address.address2
    dictionary['firma_poststed'] = current_user.company.address.post_area
    dictionary[
        'firma_postnummer'] = current_user.company.address.post_code
    return dictionary


@app.route('/json/heating/', methods=['POST', 'GET'])
@limiter.limit("1/second", error_message='Èn per sekund')
@limiter.limit("5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
def json_fill_document():
    """Fill a form from user."""
    form = forms.HeatingFmrm()
    if request.method == 'GET':
        filled_form_modified_id = request.args.get('filled_form_modified_id')
        filled_form_modified = FilledFormModified\
            .query\
            .filter(
                FilledFormModified.id == filled_form_modified_id
            )\
            .first()
        # form = FormField(manufacturor)
        # form.set_fields_from_dict(dictionary)
        form_data = filled_form_modified.form_data
        request_form = filled_form_modified.request_form
        product = Product\
            .query\
            .filter(
                Product.id == request_form['product_id']
            ).first()
        manufacturor = product.product_type.manufacturor.name
        output_pdf, dictionary, form = create_form(  # noqa
            manufacturor=manufacturor,
            form_data=form_data,
            request_form=request_form,
            user=filled_form_modified.user
        )
        return jsonify(
            file_download=os.path.relpath(output_pdf),
        )
    if request.method == 'POST':
        print(request.form)
        error_fields = validate_fields(request.form)

        if error_fields:
            return jsonify(
                error_fields=error_fields,
                error_message='Noen felt var ikke tilstrekkelig utfylt',
                status=400
            )
        product_id = request.form['product_id']
        product = Product.get_by_id(product_id)
        manufacturor = product.product_type.manufacturor.name
        dictionary = request.form.copy()

        if product:
            dictionary = set_fields_from_product(
                dictionary, product)
        else:
            return jsonify(
                error_message=(
                    "Fant ingen varmekabler med denne id '{}'. "
                    "Om dette er en feil, bør dette rapporteres."
                ).format(manufacturor),
                status=400)
        if current_user.is_authenticated:
            if current_user.company:
                dictionary = add_company_info_to_dictionary(
                    dictionary, current_user.company)

        output_pdf, complete_dictionary, form = create_form(
            manufacturor=manufacturor,
            dictionary=dictionary,
            request_form=request.form
        )
        address = Address.update_or_create(
            address_id=dictionary.get('address_id'),
            address1=dictionary.get('anleggs_adresse'),
            address2=None,
            post_code=dictionary.get('anleggs_postnummer'),
            post_area=dictionary.get('anleggs_poststed')
        )
        save_form = FilledForm.update_or_create(
            filled_form_modified_id=dictionary.get('filled_form_modified_id'),
            user=current_user,
            name=dictionary.get('rom_navn'),
            customer_name=dictionary.get('kunde_navn'),
            request_form=request.form,
            form_data=complete_dictionary,
            company=current_user.company,
            address=address
        )
        db.session.commit()

        return jsonify(
            file_download=os.path.relpath(output_pdf),
            status=200,
            filled_form_id=save_form.id,
            address_id=address.id,
        )


@app.route('/')
def view_form(dictionary=None, error_fields=None, error_message=None):
    """View for home."""
    # Set up some defaults. (retrieve this from the user-config later.)
    form = forms.HeatingForm()
    customerForm = forms.CustomerForm()
    if dictionary is None:
        dictionary = {
            'anleggs_postnummer': 4626,
            'anleggs_poststed': 'Kristiansand',
            'meterEffekt':  "17",
            'manufacturor':  "Nexans"
        }
    return render_template('main.html', form=form, customerForm=customerForm)


@login_required
@limiter.limit("200/minute", error_message='200 per minutt')
@app.route('/address/')
def search_address():
    """Search a partial address (near user)."""
    kwargs = {}
    if current_user.company:
        if False and current_user.company.lat and current_user.company.lng:
            kwargs['near_geo'] = [
                float(current_user.company.lat),
                float(current_user.company.lng)
            ]
        else:
            kwargs['near_post_code'] = current_user.company.address.post_code
    # Make sure 'post_code' is an int.
    print(request.args.get('p'))
    try:
        post_code = request.args.get('p')
        if post_code:
            kwargs['near_post_code'] = int(post_code)
    except ValueError:
        pass
    kwargs['street_name'] = request.args.get('q')
    # Try to get a valid address from search-query
    print(kwargs)
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
            Scss(app, static_dir='static/css/', asset_dir='assets/scss/')
            app.run(host='0.0.0.0', port=app.config['PORT'])
