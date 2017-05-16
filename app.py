"""Udacity assignment for creating a Neighborhood-map."""

from config import configure_app
from vk_objects import nexans
from flask import (
    Flask,
    request,
    render_template,
)


app = Flask(__name__, instance_relative_config=True)
configure_app(app)


@app.route('/')
def view_form():
    """View for home."""
    return render_template(
        'form.html',
    )


@app.route('/nexans.html', methods=['POST'])
def fill_document():
    """Fill a document with data from form, and smart usage."""
    print(request.form)
    areal = float(request.form['areal'])
    effekt = float(request.form['effekt'])
    meterEffekt = float(request.form['meterEffekt'])
    nexans.set_field('areal', areal)
    nexans.set_field('type_og_effekt', 'TXLP {}'.format(effekt))
    nexans.set_field('meterEffekt', meterEffekt)
    nexans.create_filled_pdf('output.pdf')
    return render_template(
        'form.html',
    )


# hook up extensions to app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=app.config['PORT'])
