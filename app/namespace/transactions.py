from datetime import datetime, timedelta
from http import HTTPStatus

from flask import request
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import IntegrityError

from app.constant.system_constants import SYSTEM_USER_NAME
from app.controller.transaction_controller import add_transaction
from app.db.models.models import TransactionModel, TransactionCategoryModel, TransactionTypeModel, \
    TransactionSourceModel
from app.lib.log_utils import logger
from app.utils.db_connection import DBSession

transaction_api = Namespace(name="Transactions",
                            path="/transaction",
                            description="Operations related to financial transactions",
                            strict_slashes=False)

# --- API Model Definitions ---
# Model for creating or updating a transaction
transaction_input_model = transaction_api.model('TransactionInput', {
    'transaction_date': fields.String(required=True, description='Date of the transaction (MM/DD/YYYY)',
                                      example='10/27/2023'),
    'description': fields.String(required=False, description='Transaction description', example='Coffee Shop'),
    'notes': fields.String(description='Additional notes', example='Meeting with client'),
    'category_level1': fields.String(required=False, description='Primary category', example='Business'),
    'category_level2': fields.String(required=False, description='Secondary category', example='Meals'),
    'type_name': fields.String(required=False, description='Transaction type', example='Expense'),
    'amount': fields.Float(required=False, description='Transaction amount', example=5.75),
    'source': fields.String(required=False, description='Source of funds', example='Corporate Card'),
})

# Model for serializing a transaction as output
transaction_output_model = transaction_api.model('TransactionOutput', {
    'transaction_id': fields.Integer(readonly=True, description='The unique identifier of a transaction'),
    'transaction_date': fields.Date(description='Date of the transaction'),
    'description': fields.String(description='Transaction description'),
    'notes': fields.String(description='Additional notes'),
    'category_level1': fields.String(description='Primary category'),
    'category_level2': fields.String(description='Secondary category'),
    'type_name': fields.String(description='Transaction type'),
    'amount': fields.Float(description='Transaction amount'),
    'source': fields.String(description='Source of funds'),
    'modified_at': fields.DateTime(description='Last modification timestamp'),
})


@transaction_api.route('/')
class TransactionList(Resource):
    """Handles listing transactions and creating new ones in bulk."""

    @DBSession.class_method
    @transaction_api.marshal_list_with(transaction_output_model)
    @transaction_api.doc(params={
        'period': {'description': "Filter by period ('1Mo', '3Mo', '1Yr', etc.) or 'All'. Defaults to 'All'.",
                   'in': 'query', 'type': 'string'}
    })
    def get(self, session):
        """Retrieves transaction records, optionally filtered by period.
        """
        period = request.args.get("period", "All").strip()
        query = session.query(TransactionModel)

        period_map_days = {
            '1Mo': 30, '3Mo': 90, '6Mo': 180, '1Yr': 365, '3Yr': 1095, '5Yr': 1825
        }
        days = period_map_days.get(period)
        if days:
            start_date = datetime.now() - timedelta(days=days)
            query = query.filter(TransactionModel.transaction_date >= start_date)

        return query.order_by(TransactionModel.transaction_date.desc()).all()

    @DBSession.class_method
    @transaction_api.expect([transaction_input_model], validate=True)
    def post(self, session):
        """Creates one or more new transaction records in a single batch."""
        try:
            request_body = transaction_api.payload

            # 1. Collect all unique, non-empty foreign key values from the payload
            categories = set(d.get('category_level1') for d in request_body if d.get('category_level1'))
            categories.update(d.get('category_level2') for d in request_body if d.get('category_level2'))
            types = set(d.get('type_name') for d in request_body if d.get('type_name'))
            sources = set(d.get('source') for d in request_body if d.get('source'))

            # 2. Find which ones already exist in the database
            existing_categories = {c.category for c in session.query(TransactionCategoryModel).filter(
                TransactionCategoryModel.category.in_(categories))}
            existing_types = {t.type_name for t in
                              session.query(TransactionTypeModel).filter(TransactionTypeModel.type_name.in_(types))}
            existing_sources = {s.source for s in session.query(TransactionSourceModel).filter(
                TransactionSourceModel.source.in_(sources))}

            # 3. Determine which ones are new and add them to the session
            new_categories = [TransactionCategoryModel(category=c) for c in categories if c not in existing_categories]
            new_types = [TransactionTypeModel(type_name=t) for t in types if t not in existing_types]
            new_sources = [TransactionSourceModel(source=s) for s in sources if s not in existing_sources]

            if new_categories:
                logger.info(f"Creating new categories: {[c.category for c in new_categories]}")
                session.add_all(new_categories)
            if new_types:
                logger.info(f"Creating new types: {[t.type_name for t in new_types]}")
                session.add_all(new_types)
            if new_sources:
                logger.info(f"Creating new sources: {[s.source for s in new_sources]}")
                session.add_all(new_sources)

            for transaction_data in request_body:
                add_transaction(session, transaction_data)

            # The DBSession decorator will handle the commit
            return {'message': f"Successfully processed {len(request_body)} transaction(s)."}, HTTPStatus.CREATED
        except Exception as e:
            logger.error(f"Create transaction failed: {e}")
            transaction_api.abort(HTTPStatus.INTERNAL_SERVER_ERROR, f"Could not create transaction: {e}")


@transaction_api.route('/<int:transaction_id>')
@transaction_api.response(HTTPStatus.NOT_FOUND, 'Transaction not found.')
@transaction_api.param('transaction_id', 'The unique identifier of the transaction.')
class Transaction(Resource):
    """Handles operations for a single transaction."""

    @DBSession.class_method
    @transaction_api.marshal_with(transaction_output_model)
    def get(self, session, transaction_id: int):
        """Retrieves a specific transaction by its ID."""
        transaction = session.query(TransactionModel).get(transaction_id)
        if not transaction:
            transaction_api.abort(HTTPStatus.NOT_FOUND, f"Transaction with id {transaction_id} not found.")
        return transaction

    @DBSession.class_method
    @transaction_api.expect(transaction_input_model, validate=True)
    @transaction_api.marshal_with(transaction_output_model)
    def put(self, session, transaction_id: int):
        """Updates an existing transaction record."""
        transaction_to_update = session.query(TransactionModel).get(transaction_id)
        if not transaction_to_update:
            transaction_api.abort(HTTPStatus.NOT_FOUND, f"Transaction with id {transaction_id} not found.")

        data = transaction_api.payload
        for key, value in data.items():
            setattr(transaction_to_update, key, value)

        transaction_to_update.modified_at = datetime.now()
        transaction_to_update.modified_by = SYSTEM_USER_NAME

        try:
            session.commit()
            return transaction_to_update
        except IntegrityError as e:
            transaction_api.abort(HTTPStatus.CONFLICT, f"Database integrity error: {e.orig}")
        except Exception as e:
            transaction_api.abort(HTTPStatus.INTERNAL_SERVER_ERROR, f"Could not update transaction: {e}")

    @DBSession.class_method
    @transaction_api.response(HTTPStatus.NO_CONTENT, 'Transaction deleted successfully.')
    def delete(self, session, transaction_id: int):
        """Deletes a transaction record."""
        transaction_to_delete = session.query(TransactionModel).get(transaction_id)
        if not transaction_to_delete:
            transaction_api.abort(HTTPStatus.NOT_FOUND, f"Transaction with id {transaction_id} not found.")
        try:
            session.delete(transaction_to_delete)
            return {"message": f"Transaction with id {transaction_id} deleted successfully."}, HTTPStatus.OK
        except Exception as e:
            transaction_api.abort(HTTPStatus.INTERNAL_SERVER_ERROR, f"Could not delete transaction: {e}")
