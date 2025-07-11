from flask_restx import Resource, Namespace

from db.models.models import TransactionCategoryModel
from utils.db_connection import DBSession

transaction_category_api = Namespace(name="Transaction Category",
                                     description="Edit Transaction Category",
                                     path="/")


class TransactionCategory(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        category_records = session.query(TransactionCategoryModel).all()
        print(category_records)

    @DBSession.class_method
    def post(self, session):
        category_records = session.query(TransactionCategoryModel).all()
        print(category_records)

    @DBSession.class_method
    def put(self, session):
        category_records = session.query(TransactionCategoryModel).all()
        print(category_records)

    @DBSession.class_method
    def delete(self, session):
        category_records = session.query(TransactionCategoryModel).all()
        print(category_records)
