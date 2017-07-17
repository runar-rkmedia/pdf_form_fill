"""Set up configuration."""
import os


class BaseConfig(object):
    """Base Config."""
    DEBUG = False
    TESTING = False
    PORT = int(os.environ.get("PORT", 5000))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgres:///varmekabler')
    SQLALCHEMY_BINDS = {
        'products': os.environ.get(
            'PRODUCT_DATABASE_URL', 'postgres:///vk_products'),
    }
    G_CLIENT_ID = os.environ.get(
        'G_CLIENT_ID', 'postgres:///varmekabler')
    G_CLIENT_SECRET = os.environ.get(
        'G_CLIENT_SECRET', '')
    OAUTHLIB_INSECURE_TRANSPORT = os.environ.get(
        'OAUTHLIB_INSECURE_TRANSPORT', '')
    USER_FILES = os.environ.get(
        'user_files', 'user_files')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get(
        'SECRET_KEY', 'dev')
    USE_SESSION_FOR_NEXT = True


class DevelopmentConfig(BaseConfig):
    """Configuration for development."""
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'dev'


class TestingConfig(BaseConfig):
    """Configuration for testing."""
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgres:///test_varmekabler')
    SQLALCHEMY_BINDS = {
        'products': os.environ.get(
            'PRODUCT_DATABASE_URL', 'postgres:///vk_products'),
        'forms': os.environ.get(
            'FORM_DATABASE_URL', 'postgres:///test_vk_forms'),
    }
    SECRET_KEY = 'test'
    DEBUG = False
    TESTING = True


config = {
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "default": "config.DevelopmentConfig"
}


def configure_app(app, configuration=None):
    """Retrieve configuration based on situation(dev,testing,production)."""
    config_name = os.getenv('FLASK_CONFIGURATION', configuration or 'default')
    print("Configuring app with '{}'-config.".format(config_name))
    app.config.from_object(config[config_name])
    required_keys = ['SQLALCHEMY_DATABASE_URI']
    app.config.from_pyfile('config.cfg', silent=True)
    for key in required_keys:
        if not app.config[key]:
            raise ValueError(
                "Required key '{}' missing. See Readme".format(key)
            )
