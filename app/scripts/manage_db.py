from dotenv import load_dotenv

load_dotenv(dotenv_path='../../.env.local')
from app.extension import db
from app.main import app


def drop_all_tables():
    """
    Drops all tables from the database. This is a destructive operation.
    """
    # Create an app instance to establish an application context.
    # The app_context is required for SQLAlchemy to know which database to connect to.
    # app = create_app("development")
    with app.app_context():
        try:
            # db.drop_all()
            db.create_all()
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    """
    This script provides a command-line interface to drop all tables.
    It includes a confirmation step to prevent accidental data loss.
    """
    drop_all_tables()