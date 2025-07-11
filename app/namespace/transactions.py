from datetime import datetime, timedelta
from http import HTTPStatus

from flask import make_response, jsonify, request
from flask_restx import Resource, Namespace, reqparse
from sqlalchemy.exc import IntegrityError

from app.constant.system_constants import SYSTEM_USER_NAME
from app.db.models.models import TransactionModel
from app.utils.db_connection import DBSession

transaction_api = Namespace(name="Transaction",
                            path="/",
                            description="Operations related to financial transactions")

transaction_parser = reqparse.RequestParser()
transaction_parser.add_argument('transaction_id', type=int, required=True, help='Transaction ID cannot be blank!')
transaction_parser.add_argument('transaction_date', type=str, required=False, help='Transaction Date')
transaction_parser.add_argument('description', type=str, required=False, help='Description')
transaction_parser.add_argument('notes', type=str, required=False, help='Notes')
transaction_parser.add_argument('category_level1', type=str, required=False, help='Category Level 1')
transaction_parser.add_argument('category_level2', type=str, required=False, help='Category Level 2')
transaction_parser.add_argument('type_name', type=str, required=False, help='Transaction Type')
transaction_parser.add_argument('amount', type=float, required=False, help='Amount')
transaction_parser.add_argument('source', type=str, required=False, help='Source')


class Transaction(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        """Retrieves transaction records, optionally filtered by period.

        Query Parameters:
            period (str, optional): Filter transactions by period (e.g., '1Mo', '3Mo', '6Mo', '1Yr', '3Yr', '5Yr', 'All'). Defaults to 'All'.

        Returns:
            JSON: A list of transaction objects.
        """
        period = request.args.get("period", "All")
        end_date = datetime.now()
        if period == '1Mo':
            start_date = end_date - timedelta(days=30)
            trans_records = session.query(TransactionModel).filter(
                TransactionModel.transaction_date >= start_date).all()
        elif period == '3Mo':
            start_date = end_date - timedelta(days=90)
            trans_records = session.query(TransactionModel).filter(
                TransactionModel.transaction_date >= start_date).all()
        elif period == '6Mo':
            start_date = end_date - timedelta(days=180)
            trans_records = session.query(TransactionModel).filter(
                TransactionModel.transaction_date >= start_date).all()
        elif period == '1Yr':
            start_date = end_date - timedelta(days=365)
            trans_records = session.query(TransactionModel).filter(
                TransactionModel.transaction_date >= start_date).all()
        elif period == '3Yr':
            start_date = end_date - timedelta(days=365 * 3)
            trans_records = session.query(TransactionModel).filter(
                TransactionModel.transaction_date >= start_date).all()
        elif period == '5Yr':
            start_date = end_date - timedelta(days=365 * 5)
            trans_records = session.query(TransactionModel).filter(
                TransactionModel.transaction_date >= start_date).all()
        else:
            trans_records = session.query(TransactionModel).all()
        response = []
        for record in trans_records:
            resp_obj = {
                "id": record.transaction_id,
                "Transaction Date": str(record.transaction_date),
                "Memo": record.notes,
                "Description": record.description,
                "category_level1": record.category_level1,
                "Category": record.category_level2,
                "Type": record.type_name,
                "Amount": record.amount,
                "Source": record.source
            }
            response.append(resp_obj)
        return make_response(jsonify(response), HTTPStatus.OK)

    @DBSession.class_method
    def post(self, session):
        """Creates one or more new transaction records.

        Request Body (list of dict):
            transaction_date (str, required): Date of the transaction (YYYY-MM-DD).
            description (str, required): Description of the transaction.
            notes (str, optional): Additional notes for the transaction.
            category_level1 (str, required): Primary category level.
            category_level2 (str, required): Secondary category level.
            type (str, required): Type of transaction (e.g., 'Sale', 'Expense').
            amount (float, required): Amount of the transaction.
            source (str, required): Source of the transaction (e.g., 'Credit Card', 'Cash').

        Returns:
            JSON: A message indicating success or failure.
        """
        try:
            request_body = request.json
            print(request_body)
            new_trans_list = []
            for records in request_body:
                new_trans = TransactionModel(
                    transaction_date=datetime.strptime(records.get("transaction_date"), '%Y-%m-%d') if records.get(
                        "transaction_date") else None,
                    description=records.get("description", ""),
                    notes=records.get("notes", ""),
                    category_level1=records.get("category_level1", ""),
                    category_level2=records.get("category_level2", ""),
                    type_name=records.get("type", ""),  # Changed 'type' to 'type_name'
                    amount=records.get("amount", ""),
                    source=records.get("source", ""),
                    created_at=datetime.now(),
                    created_by=SYSTEM_USER_NAME,
                    modified_at=datetime.now(),
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
        """Updates an existing transaction record.

        Request Body:
            transaction_id (int, required): The ID of the transaction to update.
            transaction_date (str, optional): New date of the transaction (YYYY-MM-DD).
            description (str, optional): New description of the transaction.
            notes (str, optional): New notes for the transaction.
            category_level1 (str, optional): New primary category level.
            category_level2 (str, optional): New secondary category level.
            type_name (str, optional): New type of transaction.
            amount (float, optional): New amount of the transaction.
            source (str, optional): New source of the transaction.

        Returns:
            JSON: A message indicating success or failure.
        """
        args = transaction_parser.parse_args()
        transaction_id = args['transaction_id']

        transaction_to_update = session.query(TransactionModel).filter_by(transaction_id=transaction_id).first()
        if not transaction_to_update:
            return make_response(jsonify({"message": f"Transaction with ID {transaction_id} not found."}),
                                 HTTPStatus.NOT_FOUND)

        # Update fields if provided in the request
        if args['transaction_date']:
            transaction_to_update.transaction_date = datetime.strptime(args['transaction_date'], '%Y-%m-%d')
        if args['description']:
            transaction_to_update.description = args['description']
        if args['notes']:
            transaction_to_update.notes = args['notes']
        if args['category_level1']:
            transaction_to_update.category_level1 = args['category_level1']
        if args['category_level2']:
            transaction_to_update.category_level2 = args['category_level2']
        if args['type_name']:
            transaction_to_update.type_name = args['type_name']
        if args['amount']:
            transaction_to_update.amount = args['amount']
        if args['source']:
            transaction_to_update.source = args['source']

        transaction_to_update.modified_at = datetime.now()
        transaction_to_update.modified_by = SYSTEM_USER_NAME

        try:
            session.commit()
            return make_response(jsonify({"message": f"Transaction with ID {transaction_id} updated successfully."}),
                                 HTTPStatus.OK)
        except IntegrityError:
            session.rollback()
            return make_response(
                jsonify({"message": "Database error: Could not update transaction."}),
                        HTTPStatus.INTERNAL_SERVER_ERROR)
