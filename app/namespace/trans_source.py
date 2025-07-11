from http import HTTPStatus

from flask import make_response, jsonify
from flask_restx import Resource, Namespace, reqparse
from sqlalchemy.exc import IntegrityError

from app.db.models.models import TransactionSourceModel
from app.utils.db_connection import DBSession

transaction_source_api = Namespace(name="Transaction Source",
                                   description="Operations related to transaction sources",
                                   path="/")

source_parser = reqparse.RequestParser()
source_parser.add_argument('source', type=str, required=True, help='Source name cannot be blank!')
source_parser.add_argument('description', type=str, required=False, help='Description of the source')


class TransactionSource(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        """Retrieves all transaction sources.

        Returns:
            JSON: A list of all transaction sources.
        """
        source_records = session.query(TransactionSourceModel).all()
        return make_response(jsonify([s.serialize for s in source_records]), HTTPStatus.OK)

    @DBSession.class_method
    def post(self, session):
        """Creates a new transaction source.

        Request Body:
            source (str, required): The name of the new source.
            description (str, optional): A description for the new source.

        Returns:
            JSON: A message indicating success or failure.
        """
        args = source_parser.parse_args()
        source_name = args['source']
        description = args['description']

        if session.query(TransactionSourceModel).filter_by(source=source_name).first():
            return make_response(jsonify({"message": f"Source '{source_name}' already exists."}), HTTPStatus.CONFLICT)

        new_source = TransactionSourceModel(source=source_name, description=description)
        try:
            session.add(new_source)
            session.commit()
            return make_response(jsonify({"message": f"Source '{source_name}' created successfully."}),
                                 HTTPStatus.CREATED)
        except IntegrityError:
            session.rollback()
            return make_response(jsonify({"message": "Database error: Could not create source."}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"message": f"An unexpected error occurred: {str(e)}"}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @DBSession.class_method
    def put(self, session):
        """Updates an existing transaction source.

        Request Body:
            source (str, required): The name of the source to update.
            description (str, optional): The new description for the source.

        Returns:
            JSON: A message indicating success or failure.
        """
        args = source_parser.parse_args()
        source_name = args['source']
        description = args['description']

        source_to_update = session.query(TransactionSourceModel).filter_by(source=source_name).first()
        if not source_to_update:
            return make_response(jsonify({"message": f"Source '{source_name}' not found."}), HTTPStatus.NOT_FOUND)

        source_to_update.description = description
        try:
            session.commit()
            return make_response(jsonify({"message": f"Source '{source_name}' updated successfully."}), HTTPStatus.OK)
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"message": f"An unexpected error occurred: {str(e)}"}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @DBSession.class_method
    def delete(self, session):
        """Deletes a transaction source.

        Request Body:
            source (str, required): The name of the source to delete.

        Returns:
            JSON: A message indicating success or failure.
        """
        args = source_parser.parse_args()
        source_name = args['source']

        source_to_delete = session.query(TransactionSourceModel).filter_by(source=source_name).first()
        if not source_to_delete:
            return make_response(jsonify({"message": f"Source '{source_name}' not found."}), HTTPStatus.NOT_FOUND)

        try:
            session.delete(source_to_delete)
            session.commit()
            return make_response(jsonify({"message": f"Source '{source_name}' deleted successfully."}), HTTPStatus.OK)
        except IntegrityError:
            session.rollback()
            return make_response(
                jsonify({"message": f"Cannot delete source '{source_name}' as it is linked to existing transactions."}),
                HTTPStatus.CONFLICT)
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"message": f"An unexpected error occurred: {str(e)}"}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
