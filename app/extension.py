from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

api = Api(version="1.0",
          title="Spending Analysis",
          description="Spending Analysis",
          prefix="",
          doc="/swagger")

cors = CORS()
db = SQLAlchemy()


def init_ext(app):
    api.init_app(app)
    db.init_app(app)
    cors.init_app(app)