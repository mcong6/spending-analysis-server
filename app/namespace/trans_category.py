from http import HTTPStatus

from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import IntegrityError

from app.db.models.models import TransactionCategoryModel
from app.utils.db_connection import DBSession

# --- API Namespace and Model Definition ---
transaction_category_api = Namespace(name="Transaction Category",
                                     description="Operations related to transaction categories",
                                     path="/transaction_category")  # Updated base path

# Define the data model for consistent input validation and output marshalling
category_model = transaction_category_api.model('TransactionCategory', {
    'id': fields.Integer(readonly=True, description='The unique identifier of a category'),
    'category': fields.String(required=True, description='Category name', example='Groceries'),
    'description': fields.String(description='Description of the category', example='Weekly food shopping')
})


# --- Resource for the Collection Endpoint (/transaction_category) ---
@transaction_category_api.route('/')
class TransactionCategoryList(Resource):
    """Handles listing all categories and creating new ones."""

    @DBSession.class_method
    @transaction_category_api.marshal_list_with(category_model)
    def get(self, session):
        """Retrieves a list of all transaction categories."""
        return session.query(TransactionCategoryModel).all()

    @DBSession.class_method
    @transaction_category_api.expect(category_model, validate=True)
    @transaction_category_api.marshal_with(category_model, code=HTTPStatus.CREATED)
    def post(self, session):
        """Creates a new transaction category."""
        data = transaction_category_api.payload
        category_name = data['category']

        if session.query(TransactionCategoryModel).filter_by(category=category_name).first():
            # Use api.abort for standard error responses
            transaction_category_api.abort(HTTPStatus.CONFLICT, f"Category '{category_name}' already exists.")

        new_category = TransactionCategoryModel(category=category_name, description=data.get('description'))

        try:
            session.add(new_category)
            session.commit()
            return new_category, HTTPStatus.CREATED
        except Exception as e:
            session.rollback()
            # It's good practice to log the actual error `e` in a real application
            transaction_category_api.abort(HTTPStatus.INTERNAL_SERVER_ERROR,
                                           "Database error: Could not create category.")


# --- Resource for the Specific Item Endpoint (/transaction_category/<id>) ---
@transaction_category_api.route('/<int:category_id>')
@transaction_category_api.response(HTTPStatus.NOT_FOUND, 'Category not found.')
@transaction_category_api.param('category_id', 'The unique identifier of the category.')
class TransactionCategory(Resource):
    """Handles operations for a single transaction category."""

    @DBSession.class_method
    @transaction_category_api.marshal_with(category_model)
    def get(self, session, category_id: int):
        """Retrieves a specific transaction category by its ID."""
        category = session.query(TransactionCategoryModel).get(category_id)
        if not category:
            transaction_category_api.abort(HTTPStatus.NOT_FOUND, f"Category with id {category_id} not found.")
        return category

    @DBSession.class_method
    @transaction_category_api.expect(category_model, validate=True)
    @transaction_category_api.marshal_with(category_model)
    def put(self, session, category_id: int):
        """Updates an existing transaction category."""
        category_to_update = session.query(TransactionCategoryModel).get(category_id)
        if not category_to_update:
            transaction_category_api.abort(HTTPStatus.NOT_FOUND, f"Category with id {category_id} not found.")

        data = transaction_category_api.payload
        category_to_update.category = data['category']
        category_to_update.description = data.get('description')

        try:
            session.commit()
            return category_to_update
        except Exception as e:
            session.rollback()
            transaction_category_api.abort(HTTPStatus.INTERNAL_SERVER_ERROR,
                                           "Database error: Could not update category.")

    @DBSession.class_method
    @transaction_category_api.response(HTTPStatus.NO_CONTENT, 'Category deleted successfully.')
    def delete(self, session, category_id: int):
        """Deletes a transaction category."""
        category_to_delete = session.query(TransactionCategoryModel).get(category_id)
        if not category_to_delete:
            transaction_category_api.abort(HTTPStatus.NOT_FOUND, f"Category with id {category_id} not found.")

        try:
            session.delete(category_to_delete)
            session.commit()
            # A 204 response should have no body
            return '', HTTPStatus.NO_CONTENT
        except IntegrityError:
            session.rollback()
            transaction_category_api.abort(HTTPStatus.CONFLICT,
                                           f"Cannot delete category '{category_to_delete.category}' as it is linked to existing transactions.")
        except Exception as e:
            session.rollback()
            transaction_category_api.abort(HTTPStatus.INTERNAL_SERVER_ERROR,
                                           "Database error: Could not delete category.")
