from http import HTTPStatus

from flask import make_response, jsonify
from flask_restx import Resource, Namespace, reqparse
from sqlalchemy.exc import IntegrityError

from app.db.models.models import TransactionCategoryModel
from app.utils.db_connection import DBSession

transaction_category_api = Namespace(name="Transaction Category",
                                     description="Operations related to transaction categories",
                                     path="/")

category_parser = reqparse.RequestParser()
category_parser.add_argument('category', type=str, required=True, help='Category name cannot be blank!')
category_parser.add_argument('description', type=str, required=False, help='Description of the category')


class TransactionCategory(Resource):
    def __init__(self, *args, **kwargs):
        Resource.__init__(*args, **kwargs)

    @DBSession.class_method
    def get(self, session):
        """Retrieves all transaction categories.

        Returns:
            JSON: A list of all transaction categories.
        """
        category_records = session.query(TransactionCategoryModel).all()
        return make_response(jsonify([c.serialize for c in category_records]), HTTPStatus.OK)

    @DBSession.class_method
    def post(self, session):
        """Creates a new transaction category.

        Request Body:
            category (str, required): The name of the new category.
            description (str, optional): A description for the new category.

        Returns:
            JSON: A message indicating success or failure.
        """
        args = category_parser.parse_args()
        category_name = args['category']
        description = args['description']

        if session.query(TransactionCategoryModel).filter_by(category=category_name).first():
            return make_response(jsonify({"message": f"Category '{category_name}' already exists."}),
                                 HTTPStatus.CONFLICT)

        new_category = TransactionCategoryModel(category=category_name, description=description)
        try:
            session.add(new_category)
            session.commit()
            return make_response(jsonify({"message": f"Category '{category_name}' created successfully."}),
                                 HTTPStatus.CREATED)
        except IntegrityError:
            session.rollback()
            return make_response(jsonify({"message": "Database error: Could not create category."}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"message": f"An unexpected error occurred: {str(e)}"}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @DBSession.class_method
    def put(self, session):
        """Updates an existing transaction category.

        Request Body:
            category (str, required): The name of the category to update.
            description (str, optional): The new description for the category.

        Returns:
            JSON: A message indicating success or failure.
        """
        args = category_parser.parse_args()
        category_name = args['category']
        description = args['description']

        category_to_update = session.query(TransactionCategoryModel).filter_by(category=category_name).first()
        if not category_to_update:
            return make_response(jsonify({"message": f"Category '{category_name}' not found."}), HTTPStatus.NOT_FOUND)

        category_to_update.description = description
        try:
            session.commit()
            return make_response(jsonify({"message": f"Category '{category_name}' updated successfully."}),
                                 HTTPStatus.OK)
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"message": f"An unexpected error occurred: {str(e)}"}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)

    @DBSession.class_method
    def delete(self, session):
        """Deletes a transaction category.

        Request Body:
            category (str, required): The name of the category to delete.

        Returns:
            JSON: A message indicating success or failure.
        """
        args = category_parser.parse_args()
        category_name = args['category']

        category_to_delete = session.query(TransactionCategoryModel).filter_by(category=category_name).first()
        if not category_to_delete:
            return make_response(jsonify({"message": f"Category '{category_name}' not found."}), HTTPStatus.NOT_FOUND)

        try:
            session.delete(category_to_delete)
            session.commit()
            return make_response(jsonify({"message": f"Category '{category_name}' deleted successfully."}),
                                 HTTPStatus.OK)
        except IntegrityError:
            session.rollback()
            return make_response(jsonify(
                {"message": f"Cannot delete category '{category_name}' as it is linked to existing transactions."}),
                                 HTTPStatus.CONFLICT)
        except Exception as e:
            session.rollback()
            return make_response(jsonify({"message": f"An unexpected error occurred: {str(e)}"}),
                                 HTTPStatus.INTERNAL_SERVER_ERROR)
