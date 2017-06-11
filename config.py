"""Set up configuration."""
import os


class BaseConfig(object):
    """Base Config."""
    DEBUG = False
    TESTING = False
    PORT = int(os.environ.get("PORT", 5000))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgres:///varmekabler')
    USER_FILES = os.environ.get(
        'user_files', 'user_files')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev'
    USE_SESSION_FOR_NEXT = True


class DevelopmentConfig(BaseConfig):
    """Configuration for development."""
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'dev'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class TestingConfig(BaseConfig):
    """Configuration for testing."""
    DEBUG = False
    TESTING = True


config = {
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "default": "config.DevelopmentConfig"
}


def configure_app(app):
    """Retrieve configuration based on situation(dev,testing,production)."""
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    print("Configuring app with '{}'-config.".format(config_name))
    app.config.from_object(config[config_name])
    required_keys = ['SQLALCHEMY_DATABASE_URI']
    app.config.from_pyfile('config.cfg', silent=True)
    for key in required_keys:
        if not app.config[key]:
            raise ValueError(
                "Required key '{}' missing. See Readme".format(key)
                )
