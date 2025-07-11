from flask_restx import Resource, Namespace
from flask import make_response, jsonify
from http import HTTPStatus

index_api = Namespace("", description="Root API endpoint")


class Index(Resource):
    def get(self):
        """Returns a simple welcome message for the API."""
        return make_response(jsonify("Welcome to the Spending Analysis API!"),HTTPStatus.OK)
