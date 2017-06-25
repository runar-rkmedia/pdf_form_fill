"""PDF-fill for heating cables."""
# pylama:ignore=W0512

import os
import decimal
import re
import base64

from config import configure_app
from field_dicts.helpers import (commafloat, id_generator, )
from models import (db,
                    Manufacturor,
                    Product,
                    User,
                    OAuth,
                    Invite,
                    FilledFormModified,
                    FilledForm,
                    Address
                    )
from vk_objects import FormField

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
from datetime import datetime


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


assets = Environment(app)
js_main = Bundle(
    'js/ko-bootstrap-typeahead.js',
    'js/ko.js',
    filters='jsmin',
    output='gen/packed.js')
assets.register('js_main', js_main)

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
    # legg til enleder/toleder
    ledere = product.product_type.secondSpec
    if ledere == 2:
        dictionary['check-toleder'] = True
    elif ledere == 1:
        dictionary['check-enleder'] = True

    dictionary['nominell_motstand'] = product.specs.get(
        'Nominell elementmotstand')
    dictionary['resistans_min'] = product.specs.get(
        'Resistans_min')
    dictionary['resistans_max'] = product.specs.get(
        'Resistans_max')
    dictionary['lengde'] = product.specs.get(
        'Lengde')

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
    print(invite)
    if request.method == 'POST' and invite:
        invite.invitee = current_user
        current_user.company = invite.company
        db.session.commit()
        return render_template('invite.html', invite=invite, newly_invite=True)
    return render_template('invite.html', invite=invite)


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
    request_type = request.args.get('type')
    page = request.args.get('page', 1)
    if request_type == 'company':
        forms, pages = current_user.company.get_forms(page=page)
    else:
        forms, pages = current_user.get_forms(page=page)
    if forms:
        result = {}
        result['forms'] = [i.serialize for i in forms]
        result['pages'] = pages
        return jsonify(result)
    else:
        return jsonify({})

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
    dictionary['firma_adresse1'] = current_user.company.address.line1
    dictionary['firma_adresse2'] = current_user.company.address.line2
    dictionary['firma_poststed'] = current_user.company.address.postal
    dictionary[
        'firma_postnummer'] = current_user.company.address.postnumber
    return dictionary

@app.route('/json/heating/', methods=['POST','GET'])
@limiter.limit("1/second", error_message='Èn per sekund')
@limiter.limit("5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
def json_fill_document():
    """Fill a form from user."""
    if request.method == 'GET':
        filled_form_modified_id = request.args.get('filled_form_modified_id')
        filled_form_modified = FilledFormModified\
            .query\
            .filter(
                FilledFormModified.id==filled_form_modified_id
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
        output_pdf, dictionary, form = create_form(
            manufacturor=manufacturor,
            form_data=form_data,
            request_form=request_form,
            user=filled_form_modified.user
            )
        return jsonify(
            file_download=os.path.relpath(output_pdf),
        )
    if request.method == 'POST':
        current_user.get_forms()
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
                dictionary = add_company_info_to_dictionary(dictionary, current_user.company)

        output_pdf, complete_dictionary, form = create_form(
            manufacturor=manufacturor,
            dictionary=dictionary,
            request_form=request.form
            )
        address = Address.update_or_create(
            address_id=dictionary.get('address_id'),
            line1=dictionary.get('anleggs_adresse'),
            line2=None,
            postnumber=dictionary.get('anleggs_postnummer'),
            postal=dictionary.get('anleggs_poststed')
        )
        save_form = FilledForm.update_or_create(
            filled_form_id=dictionary.get('filled_form_id'),
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
    if dictionary is None:
        dictionary = {
            'anleggs_postnummer': 4626,
            'anleggs_poststed': 'Kristiansand',
            'meterEffekt':  "17",
            'manufacturor':  "Nexans"
        }
    return render_template('main.html')


# hook up extensions to app
if __name__ == "__main__":
    if app.config['DEBUG'] is True:
        Scss(app, static_dir='static/css/', asset_dir='assets/scss/')
    app.run(host='0.0.0.0', port=app.config['PORT'])
