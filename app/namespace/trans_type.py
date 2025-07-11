from flask_restx import Resource, Namespace

from db.models.models import TransactionTypeModel
from utils.db_connection import DBSession

transaction_type_api = Namespace(name="Transaction Type",
                                 description="Edit Transaction Type",
                                 path="/")


class TransactionType(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        type_records = session.query(TransactionTypeModel).all()
        print(type_records)

    @DBSession.class_method
    def post(self, session):
        type_records = session.query(TransactionTypeModel).all()
        print(type_records)

    @DBSession.class_method
    def put(self, session):
        type_records = session.query(TransactionTypeModel).all()
        print(type_records)

    @DBSession.class_method
    def delete(self, session):
        type_records = session.query(TransactionTypeModel).all()
        print(type_records)
