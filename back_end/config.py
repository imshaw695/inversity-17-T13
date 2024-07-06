import os
from dotenv import load_dotenv

this_directory = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(this_directory, '.env'), override=True)

# if os.environ.get("INSTANCE_TYPE") == "development":
#     ssl_cert = os.path.join(this_directory, '../../HTTPS', 'localhost.pem')
#     ssl_key = os.path.join(this_directory, '../../HTTPS', 'localhost-key.pem')


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_APP = 'wsgi.py'

    # .env variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    INSTANCE_TYPE = os.environ.get('INSTANCE_TYPE')
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    DB_USERNAME = os.environ.get('DB_USERNAME')
    database_password = os.environ.get('database_password')
    database_url = os.environ.get('database_url')
    database_port = os.environ.get('database_port')
    database = os.environ.get('database')

    if os.environ.get("this_url") == "https://127.0.0.1:5000":
        # Development config
        VERIFY_SSL = False
    else:
        # Production config
        VERIFY_SSL = True

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://"
        + DB_USERNAME
        + ":"
        + database_password
        + "@"
        + database_url
        + ":" + database_port
        + "/"
        + database
    )
    # This option is specifically for PythonAnyWhere as the mysql db drops connections that are 300 seconds old
    # Inspired from here: https://stackoverflow.com/questions/56271116/flask-sqlalchemy-sqlalchemy-engine-options-not-set-up-correctly
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 240,
        'pool_pre_ping': True
    }

    support_user_email = os.environ.get('support_user_email')
    support_user_password = os.environ.get('support_user_password')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = True
    MAIL_USERNAME = support_user_email
    ADMINS = [support_user_email]

    # move the location of the staic folder for vue / vite
    STATIC_FOLDER = os.path.join(this_directory, "website", "templates", "static")
    static_folder = os.path.join(this_directory, "website", "templates", "static")
    STATIC_URL_PATH = "/static"


if __name__ == "__main__":
    config = Config()