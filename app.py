"""Udacity assignment for creating a Neighborhood-map."""

from config import configure_app
from vk_objects import nexans
from flask import (
    Flask,
    request,
    redirect,
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
    nexans.set_fields_from_dict(request.form) # TODO: is this safe?
    nexans.create_filled_pdf('output.pdf')
    return redirect('/')


# hook up extensions to app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=app.config['PORT'])
