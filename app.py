"""PDF-fill for heating cables."""

import os
import random
import string
import decimal

from config import configure_app
from field_dicts.helpers import commafloat
from models import (db, Manufacturor, lookup_vk)
from vk_objects import Nexans, Oegleand

from flask import (
    Flask,
    request,
    json,
    # redirect,
    render_template,
    send_from_directory
)
from flask_scss import Scss
from flask_assets import Environment, Bundle


class MyJSONEncoder(json.JSONEncoder):
    """Redefine flasks json-encoded to convert Decimals.."""

    def default(self, obj): # noqa
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__, instance_relative_config=True)
app.json_encoder = MyJSONEncoder
configure_app(app)




assets = Environment(app)
js = Bundle(
    'js/def.js',
    filters='jsmin', output='gen/packed.js')
assets.register('js_all', js)

css = Bundle(
    # 'css/bootstrap.min.css',
    'css/style.css',
    filters='cssmin',
    output='css/min.css'
)
assets.register('css_all', css)

db.init_app(app)


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
    dictionary["Betegnelse"] = product.name
    # legg til enleder/toleder
    ledere = product.product_type.ledere
    if ledere == 2:
        dictionary['check-toleder'] = True
    elif ledere == 1:
        dictionary['check-enleder'] = True

    for s in specs:
        if s.key == 'Nominell elementmotstand':
            dictionary['nominell_motstand'] = s.value
    return dictionary

@app.route('/products.json')
def json_products():
    """Return a json-object of all products."""
    manufacturors = Manufacturor.query.all()

    return json.jsonify([i.serialize for i in manufacturors])


@app.route('/user_files/<path:filename>', methods=['GET'])
def download(filename):
    """Serve a file for downloading."""
    return send_from_directory(directory=app.root_path, filename=filename)


@app.route('/success/')
def success(dictionary, user_file):
    """Form filled successfully, show file, or edit."""
    return render_template(
        'success.html',
        dictionary=dictionary,
        user_file=user_file
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
    return render_template(
        'form.html',
        dictionary=dictionary,
        error_fields=error_fields,
        error_message=error_message
    )


@app.route('/nexans.html', methods=['POST'])
def fill_document():
    """Fill a document with data from form, and smart usage."""
    required_fields = {
        'strings': [
            'anleggs_adresse',
            'manufacturor',
        ],
        'digits': [
            'effekt',
            'meterEffekt',
            'oppvarmet_areal'
        ]}
    error_fields = []

    for key in required_fields['strings']:
        field = request.form.get(key)
        if not field:
            error_fields.append(key)
    for key in required_fields['digits']:
        field = request.form.get(key)
        if not field:
            error_fields.append(key)
        else:
            try:
                commafloat(field)
            except ValueError:
                error_fields.append(key)

    if error_fields:
        return view_form(
            dictionary=request.form,
            error_fields=error_fields,
            error_message=None)

    vk_manufacturor = request.form['manufacturor']
    vk_effekt = request.form['effekt']
    vk_meterEffekt = request.form['meterEffekt']
    filtered_vks = lookup_vk(vk_manufacturor, vk_meterEffekt, vk_effekt)
    dictionary = request.form.copy()
    if len(filtered_vks) > 1:
        return view_form(
            dictionary=dictionary,
            error_message="Fant flere varmekabler fra {} på {} w/m, med effekten {}".format(  # noqa
                vk_manufacturor, vk_meterEffekt, vk_effekt
            ))
    elif len(filtered_vks) == 1:
        varmekabel = filtered_vks[0]
        specs = varmekabel.get_specs()
        dictionary = set_fields_from_product(
            dictionary, varmekabel, specs)
    else:
        return view_form(
            dictionary=dictionary,
            error_message="Fant ingen varmekabler fra {} på {} w/m, med effekten {}".format(  # noqa
                vk_manufacturor, vk_meterEffekt, vk_effekt
            ))
    if vk_manufacturor == 'Nexans':
        form = Nexans
    elif vk_manufacturor == 'Øglænd':
        form = Oegleand
    form.set_fields_from_dict(dictionary)
    filename = dictionary.get('anleggs_adresse', 'output') + '.pdf'
    output_path = user_file_path(filename, create_random_dir=True)
    form.create_filled_pdf(output_path)
    return success(dictionary, os.path.relpath(output_path))


# hook up extensions to app
if __name__ == "__main__":
    if app.config['DEBUG'] is True:
        Scss(app, static_dir='static/css/', asset_dir='assets/scss/')
    app.run(host='0.0.0.0', port=app.config['PORT'])
