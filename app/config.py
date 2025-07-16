import os

from sqlalchemy.pool import NullPool


def get_db_uri():
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    database = "spendingAnalysis"
    return f"postgresql://{username}:{password}@{DB_HOST}:{DB_PORT}/{database}"


class BaseConfig:
    DEBUG = False
    TESTING = False
    SQLALCEHMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_db_uri()
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_reset_on_return": "rollback",
        "poolclass": NullPool
    }


class DevelopmentConfig(BaseConfig):
    DEBUG = False


envs = {"development": DevelopmentConfig}
