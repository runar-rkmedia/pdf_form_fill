# -*- coding: utf-8 -*-

""" Bare app settings and functionality. """
import os
from config import configure_app
from functools import wraps

from flask import (Flask, flash, redirect, render_template, request,  # NOQA
                   send_from_directory, session, url_for)
from flask.json import jsonify
from sqlalchemy.orm.exc import NoResultFound

import my_exceptions
import wtforms_json
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.contrib.google import google, make_google_blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import (LoginManager, current_user, login_required,  # NOQA
                         login_user, logout_user)
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf.csrf import CSRFError, CSRFProtect
# import schemas
from models import MyJSONEncoder, db
from models_credentials import (Address, Company, Customer, Invite,  # NOQA
                                InviteType, OAuth, Room, RoomItem,
                                RoomTypeInfo, User, UserRole)
from pdf_filler.helpers import id_generator

wtforms_json.init()

app = Flask(__name__, instance_relative_config=True)
app.json_encoder = MyJSONEncoder
configure_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

db.init_app(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2000 per day", "500 per hour"])
blueprint = make_google_blueprint(
    client_id=app.config['G_CLIENT_ID'],
    client_secret=app.config['G_CLIENT_SECRET'],
    offline=True,
    scope=["profile", "email"],
    reprompt_consent=True,)
app.register_blueprint(blueprint, url_prefix="/login")

# setup login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = "Vennligst logg inn for å få adgang til denne siden."
login_manager.init_app(app)

# setup SQLAlchemy backend
blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)
csrf = CSRFProtect(app)


@app.context_processor
def include_user_roles():
    """Inlcude user role in all requests."""
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
        return render_template(
            'login_screen.html',
            redirect_url=redirect or url_for('main')
        )
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])


@oauth_authorized.connect
def logged_in(blueprint_, token):
    """User logged in."""
    next_redirect = session.get('next')
    return redirect(next_redirect or url_for('main'))


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
                email=email,)
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
    return redirect(url_for("main"))


def company_required(f):
    """Decorator for view where a user needs to have a company."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """The view we are decorating."""
        if not (
                current_user.is_authenticated and
                current_user.company
        ):
            flash(
                'Du må være registrert på et firma for å kunne bruke denne siden. Dette krever invitasjon.'  # noqa
                , 'error')
            return redirect(url_for('main'))
        return f(*args, **kwargs)
    return decorated_function


def json_ok():
    """Notify action was ok through ajax."""
    return jsonify({'status': 'OK'})


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    """Handler for csrf-errors."""
    print('csrf-error: {}'.format(e))
    return jsonify({'errors': [str(e)]})


@app.errorhandler(my_exceptions.MyBaseException)
def handle_invalid_usage(error):
    """Handler for apps exceptions."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(429)
def ratelimit_handler(e):
    """Errorhandler for ratelimiting."""
    return jsonify(
        error_message=(
            "Ta det med ro, vennligst ikke hamre i vei på serveren. "
            "Du har nådd grensen for maks antall innsendinger: {}"
        ).format(e.description),
        status=429)


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
