"""PDF-fill for heating cables."""
# pylama:ignore=W0512

import os
import random
import string
import decimal
import re
import base64

from config import configure_app
from field_dicts.helpers import commafloat
from models import (db, Manufacturor, Product, User, OAuth)
from vk_objects import FormField

from flask import (
    Flask,
    request,
    flash,
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

from sqlalchemy.orm.exc import NoResultFound
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized, oauth_error
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


class MyJSONEncoder(JSONEncoder):
    """Redefine flasks json-encoded to convert Decimals.."""

    def default(self, obj):  # noqa
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


app = Flask(__name__, instance_relative_config=True)
app.json_encoder = MyJSONEncoder
configure_app(app)


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


assets = Environment(app)
js = Bundle(
    'js/signature_pad.js',
    'js/def.js',
    'js/ko-bootstrap-typeahead.js',
    'js/ko.js',
    # filters='jsmin',
    output='gen/packed.js')
assets.register('js_all', js)

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


@login_manager.user_loader
def load_user(user_id):
    """Return user by user_id."""
    return User.query.get(int(user_id))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Return random string with digits."""
    return ''.join(random.choice(chars) for _ in range(size))


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
    ledere = product.product_type.ledere
    if ledere == 2:
        dictionary['check-toleder'] = True
    elif ledere == 1:
        dictionary['check-enleder'] = True

    for s in specs:
        if s.key == 'Nominell elementmotstand':
            dictionary['nominell_motstand'] = s.value
        if s.key == 'Resistans_min':
            dictionary['resistans_min'] = s.value
        if s.key == 'Resistans_max':
            dictionary['resistans_max'] = s.value
        if s.key == 'Lengde':
            dictionary['lengde'] = s.value
    return dictionary


def validate_fields(request_form):
    """Validate the input from a form."""
    print('validate/...')
    error_fields = []
    required_fields = {
        'strings': [
            'anleggs_adresse',
        ],
        'digits': [
            'product_id',
            'oppvarmet_areal'
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


@app.route("/login")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Du er nå logget ut")
    return redirect(url_for("view_form"))


@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):  # noqa
    """Create/login local user on successful OAuth login."""
    if not token:
        flash(
            "Feil: Kunne ikke logge på med {name}".format(name=blueprint.name))
        return
    # figure out who the user is
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    print('loggin in...')
    from pprint import pprint
    pprint(blueprint.session)
    if resp.ok:
        print(resp.json())
        name = resp.json()["name"]
        email = resp.json()["email"]
        query = User.query.filter_by(email=email)
        try:
            user = query.one()
        except NoResultFound:
            # create a user
            user = User(
                name=name,
                email=email,
                )
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash("Vellykket pålogginggjennom Google")
    else:
        msg = "Feil: Kunne ikke hente bruker-info fra {name}".format(
            name=blueprint.name)
        flash(msg, category="error")


@app.route('/set_sign', methods=['POST'])
def save_image():
    """Save an image from a data-string."""
    image_b64 = request.values['imageBase64']
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)
    imgdata = base64.b64decode(image_data)
    filename = 'some_image.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)
    return 's'


@app.route('/user_files/<path:filename>', methods=['GET'])
def download(filename):
    """Serve a file for downloading."""
    directory = os.path.join(app.root_path, app.config['USER_FILES'])
    return send_from_directory(directory=directory, filename=filename)


@app.route('/success/')
def success(dictionary, user_file):
    """Form filled successfully, show file, or edit."""
    return render_template(
        'success.html',
        dictionary=dictionary,
        user_file=user_file
    )


@app.route('/products.json')
# @limiter.limit("1/second", error_message='Èn per sekund')
@limiter.limit("5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
def json_products():
    """Return a json-object of all products."""
    manufacturors = Manufacturor.query.all()

    return jsonify([i.serialize for i in manufacturors])


@app.route('/json/heating/', methods=['POST'])
@limiter.limit("1/second", error_message='Èn per sekund')
@limiter.limit("5/10seconds", error_message='Fem per ti sekunder')
@limiter.limit("200/hour", error_message='200 per hour')
def json_fill_document():
    """Return a json-object of all products."""
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
        specs = product.get_specs()
        dictionary = set_fields_from_product(
            dictionary, product, specs)
    else:
        return jsonify(
            error_message=(
                "Fant ingen varmekabler med denne id '{}'. "
                "Om dette er en feil, bør dette rapporteres."
            ).format(manufacturor),
            status=400)
    if dictionary.get('mohm_a') == 'true':
        dictionary['mohm_a'] = 999
    if dictionary.get('mohm_b') == 'true':
        dictionary['mohm_b'] = 999
    if dictionary.get('mohm_c') == 'true':
        dictionary['mohm_c'] = 999
    print(dictionary.get('mohm_a'))
    form = FormField(manufacturor)
    form.set_fields_from_dict(dictionary)
    filename = dictionary.get('anleggs_adresse', 'output') + '.pdf'
    output_path = user_file_path(filename, create_random_dir=True)
    form.create_filled_pdf(output_path)
    form.stamp_with_image(output_path, 'some_image.png', 20, 10)

    return jsonify(
        file_download=os.path.relpath(output_path),
        status=200)


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
    return render_template('form.html')


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


# hook up extensions to app
if __name__ == "__main__":
    if app.config['DEBUG'] is True:
        Scss(app, static_dir='static/css/', asset_dir='assets/scss/')
    app.run(host='0.0.0.0', port=app.config['PORT'])
