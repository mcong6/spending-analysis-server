from flask_restx import Resource, Namespace
from flask import make_response, jsonify
from http import HTTPStatus

index_api = Namespace("", description="web api")


class Index(Resource):
    def get(self):
        return make_response(jsonify("Index page"),HTTPStatus.OK)
