from datetime import datetime, timedelta
from http import HTTPStatus

from flask import make_response, jsonify, request
from flask_restx import Resource, Namespace

from constant.system_constants import SYSTEM_USER_NAME
from db.models.models import TransactionModel
from utils.db_connection import DBSession

transaction_api = Namespace(name="Transaction",
                            path="/",
                            description="Transaction")


class Transaction(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        period = request.args.get("period", "All")
        end_date = datetime.now()
        if period == '1Mo':
            start_date = end_date - timedelta(days=30)
            trans_records=session.query(TransactionModel).filter(TransactionModel.transaction_date >= start_date).all()
        elif period == '3Mo':
            start_date = end_date - timedelta(days=90)
            trans_records=session.query(TransactionModel).filter(TransactionModel.transaction_date >= start_date).all()
        elif period == '6Mo':
            start_date = end_date - timedelta(days=180)
            trans_records=session.query(TransactionModel).filter(TransactionModel.transaction_date >= start_date).all()
        elif period == '1Yr':
            start_date = end_date - timedelta(days=365)
            trans_records=session.query(TransactionModel).filter(TransactionModel.transaction_date >= start_date).all()
        elif period == '3Yr':
            start_date = end_date - timedelta(days=365*3)
            trans_records=session.query(TransactionModel).filter(TransactionModel.transaction_date >= start_date).all()
        elif period == '5Yr':
            start_date = end_date - timedelta(days=365*5)
            trans_records=session.query(TransactionModel).filter(TransactionModel.transaction_date >= start_date).all()
        else:
            trans_records=session.query(TransactionModel).all()
        response = []
        for record in trans_records:
            resp_obj = {
                "id": record.transaction_id,
                "Transaction Date": str(record.transaction_date),
                "Memo": record.notes,
                "Description": record.description,
                "category_level1": record.category_level1,
                "Category": record.category_level2,
                "Type": record.type,
                "Amount": record.amount,
                "Source": record.source
            }
            response.append(resp_obj)
        return make_response(jsonify(response), HTTPStatus.OK)

    @DBSession.class_method
    def post(self, session):
        """{transcation}"""
        try:
            request_body = request.json
            print(request_body)
            new_trans_list = []
            for records in request_body:
                new_trans = TransactionModel(
                    transaction_date=records.get("transaction_date", ""),
                    description=records.get("description", ""),
                    notes=records.get("notes", ""),
                    category_level1=records.get("category_level1", ""),
                    category_level2=records.get("category_level2", ""),
                    type=records.get("type", ""),
                    amount=records.get("amount", ""),
                    source=records.get("source", ""),
                    created_at=str(datetime.now()),
                    created_by=SYSTEM_USER_NAME,
                    modified_at=str(datetime.now()),
                    modified_by=SYSTEM_USER_NAME
                )
                new_trans_list.append(new_trans)
                session.add(new_trans)
            session.commit()
            return make_response(jsonify(f"Upload files successfully."), HTTPStatus.OK)
        except Exception as e:
            return make_response(jsonify(f"Upload files failed. {str(e)}"), HTTPStatus.BAD_REQUEST)

    @DBSession.class_method
    def put(self, session):
        trans_records = session.query(TransactionModel).all()
        print(trans_records)

    @DBSession.class_method
    def delete(self, session):
        trans_records = session.query(TransactionModel).all()
        print(trans_records)
