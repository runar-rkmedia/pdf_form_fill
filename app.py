"""PDF-fill for heating cables."""

import sys
import os

from config import configure_app
from helpers import commafloat
from models import (db, Manufacturor, Product,
                    ProductSpec, ProductType, lookup_vk)
from vk_objects import nexans
from flask import (
    Flask,
    request,
    redirect,
    render_template,
    send_from_directory
)
from flask_scss import Scss
from flask_assets import Environment, Bundle


app = Flask(__name__, instance_relative_config=True)
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


def user_file_path(filename=None):
    """Return full path to user-directory."""
    paths = [app.root_path, app.config['USER_FILES']]
    if filename:
        paths.append(filename)
    return os.path.join(*paths)


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


@app.route('/user_files/<path:filename>', methods=['GET'])
def download(filename):
    """Serve a file for downloading."""
    user_files = user_file_path()
    print(user_files)
    return send_from_directory(directory=user_files, filename=filename)


@app.route('/success/')
def success(dictionary, user_file):
    """Form filled successfully, show file, or edit."""
    return render_template(
        'success.html',
        dictionary=dictionary,
        user_file=user_file
    )


@app.route('/')
def view_form(dictionary=None, error_fields=[], error_message=None):
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

    nexans.set_fields_from_dict(dictionary)
    filename = dictionary.get('anleggs_adresse', 'output') + '.pdf'
    output_path = user_file_path(filename)
    print(output_path)
    nexans.create_filled_pdf(output_path)
    return success(dictionary, filename)


# hook up extensions to app
if __name__ == "__main__":
    if '--setup' in sys.argv:
        print('Setup')
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        with app.app_context():
            db.drop_all()
            db.create_all()
            Nexans = Manufacturor(name='Nexans', description="It's nexans")
            db.session.add(Nexans)
            txlp17 = ProductType(name='TXLP/2R/17',
                                 mainSpec='TXLP',
                                 watt_per_meter=17,
                                 ledere=2,
                                 manufacturor=Nexans)
            txlp10 = ProductType(name='TXLP/2R/10',
                                      mainSpec='TXLP',
                                      watt_per_meter=10,
                                      ledere=2,
                                      manufacturor=Nexans)
            db.session.add(txlp17)
            db.session.add(txlp10)
            import Nexans_TXLP
            for vk in Nexans_TXLP.vks:
                name = vk.pop('Betegnelse')
                effekt = vk.pop('Effekt ved 230V')
                if name[-2:] == '17':
                    product_type = txlp17
                else:
                    product_type = txlp10
                if name:
                    new_vk = Product(
                        name=name, product_type=product_type, effekt=effekt)
                    new_vk.add_keys_from_dict(vk)
                    db.session.add(new_vk)
            tulle_vk = Product(
                name='TULL', product_type=txlp10, effekt=500)
            db.session.add(tulle_vk)
            db.session.commit()
            print("Database tables created")

    else:
        if app.config['DEBUG'] is True:
            Scss(app, static_dir='static/css/', asset_dir='assets/scss/')
        app.run(host='0.0.0.0', port=app.config['PORT'])
