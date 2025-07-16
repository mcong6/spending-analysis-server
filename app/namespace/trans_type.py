from http import HTTPStatus

from flask import make_response, jsonify
from flask_restx import Resource, Namespace, reqparse
from sqlalchemy.exc import IntegrityError

from app.db.models.models import TransactionTypeModel
from app.utils.db_connection import DBSession

transaction_type_api = Namespace(name="Transaction Type",
                                 description="Operations related to transaction types",
                                 path="/transaction_type")

type_parser = reqparse.RequestParser()
type_parser.add_argument('type_name', type=str, required=True, help='Type name cannot be blank!')
type_parser.add_argument('description', type=str, required=False, help='Description of the type')


class TransactionType(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        """Retrieves all transaction types.

        Returns:
            JSON: A list of all transaction types.
        """
        type_records = session.query(TransactionTypeModel).all()
        return make_response(jsonify([t.serialize for t in type_records]), HTTPStatus.OK)

    @DBSession.class_method
    def post(self, session):
        """Creates a new transaction type.

        Request Body:
            type_name (str, required): The name of the new type.
            description (str, optional): A description for the new type.

        Returns:
            JSON: A message indicating success or failure.
        """
        args = type_parser.parse_args()
        type_name = args['type_name']
        description = args['description']

        if session.query(TransactionTypeModel).filter_by(type_name=type_name).first():
            return make_response(jsonify({"message": f"Type '{type_name}' already exists."}), HTTPStatus.CONFLICT)

        new_type = TransactionTypeModel(type_name=type_name, description=description)
        try:
            session.add(new_type)
            session.commit()
            return make_response(jsonify({"message": f"Type '{type_name}' created successfully."}), HTTPStatus.CREATED)
        except IntegrityError:
            session.rollback()
            return make_response(jsonify({"message": "Database error: Could not create type."}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"message": f"An unexpected error occurred: {str(e)}"}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @DBSession.class_method
    def put(self, session):
        """Updates an existing transaction type.

        Request Body:
            type_name (str, required): The name of the type to update.
            description (str, optional): The new description for the type.

        Returns:
            JSON: A message indicating success or failure.
        """
        args = type_parser.parse_args()
        type_name = args['type_name']
        description = args['description']

        type_to_update = session.query(TransactionTypeModel).filter_by(type_name=type_name).first()
        if not type_to_update:
            return make_response(jsonify({"message": f"Type '{type_name}' not found."}), HTTPStatus.NOT_FOUND)

        type_to_update.description = description
        try:
            session.commit()
            return make_response(jsonify({"message": f"Type '{type_name}' updated successfully."}), HTTPStatus.OK)
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"message": f"An unexpected error occurred: {str(e)}"}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @DBSession.class_method
    def delete(self, session):
        """Deletes a transaction type.

        Request Body:
            type_name (str, required): The name of the type to delete.

        Returns:
            JSON: A message indicating success or failure.
        """
        args = type_parser.parse_args()
        type_name = args['type_name']

        type_to_delete = session.query(TransactionTypeModel).filter_by(type_name=type_name).first()
        if not type_to_delete:
            return make_response(jsonify({"message": f"Type '{type_name}' not found."}), HTTPStatus.NOT_FOUND)

        try:
            session.delete(type_to_delete)
            session.commit()
            return make_response(jsonify({"message": f"Type '{type_name}' deleted successfully."}), HTTPStatus.OK)
        except IntegrityError:
            session.rollback()
            return make_response(
                jsonify({"message": f"Cannot delete type '{type_name}' as it is linked to existing transactions."}),
                HTTPStatus.CONFLICT)
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"message": f"An unexpected error occurred: {str(e)}"}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
