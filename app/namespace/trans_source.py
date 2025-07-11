from flask_restx import Resource, Namespace

from db.models.models import TransactionSourceModel
from utils.db_connection import DBSession

transaction_source_api = Namespace(name="Transaction Source",
                                   description="Edit Transaction Source",
                                   path="/")


class TransactionSource(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        source_records = session.query(TransactionSourceModel).all()
        print(source_records)

    @DBSession.class_method
    def post(self, session):
        source_records = session.query(TransactionSourceModel).all()
        print(source_records)

    @DBSession.class_method
    def put(self, session):
        source_records = session.query(TransactionSourceModel).all()
        print(source_records)

    @DBSession.class_method
    def delete(self, session):
        source_records = session.query(TransactionSourceModel).all()
        print(source_records)
