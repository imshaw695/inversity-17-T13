import os
import platform
import socket
from flask import Flask
from flask_talisman import Talisman

site_config = {}
site_config["platform"] = platform.system()
site_config["base_directory"] = os.path.abspath(os.path.dirname(__file__))
site_config["host_name"] = socket.gethostname()
site_config[
    "environment"
] = f'host:{site_config["host_name"]}, platform:{site_config["platform"]}'
site_config["INSTANCE_TYPE"] = os.environ.get("INSTANCE_TYPE")
site_config["this_url"] = os.environ.get("this_url")

def create_app():
    print("now running create_app")
    # Create Flask application.
    # this_directory = os.path.abspath(os.path.dirname(__file__))
    this_directory = os.path.abspath(os.path.dirname(__file__))
    static_folder = os.path.join(this_directory, "templates", "static")
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder=static_folder,
        static_url_path="/static",
    )
    try:
        app.config.from_object("config.Config")
    except Exception as err:
        print(f'On line 54 the error is {err}')

    with app.app_context():
        SELF = "'self'"
        csp = {
            "default-src": "'self'",
            "img-src": "*",
            'connect-src': [
                SELF,
            ],
            'style-src' : [
            SELF,
            '\'unsafe-inline\''
            ]
        }
        talisman = Talisman(app, content_security_policy=csp)

        from website import routes

        return app