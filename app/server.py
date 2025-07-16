from flask import Flask

from app.apis import init_api
from app.config import envs
from app.extension import init_ext, api
from app.lib.json_processor import CustomJSONProvider


def create_app(environment):
    print("create application")
    app = Flask(__name__)
    app.config.from_object(envs.get(environment))
    app.json = CustomJSONProvider(app)
    api.app = app
    init_api(api)
    init_ext(app)
    return app
