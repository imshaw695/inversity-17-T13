import os

class Config:

    FLASK_APP = 'wsgi.py'

    INSTANCE_TYPE = os.environ.get('INSTANCE_TYPE')
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":

    # test to see that config is working 
    config = Config()
    keys = config.__dir__()
    for key in keys:
        if key[0:2] != "__":
            value = config.__getattribute__(key)
            if isinstance(value, str):
                print(f"key: {key}    value: {value}")