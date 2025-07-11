from http import HTTPStatus
from flask import make_response, jsonify


class ClientException(BaseException):
    # def __init__(self, *args, **kwargs):  # real signature unknown
    #     pass

    def __init__(self, value):
        self.value = value

    # @staticmethod  # known case of __new__
    # def __new__(*args, **kwargs):  # real signature unknown
    #     """ Create and return a new object.  See help(type) for accurate signature. """
    #     pass

    def __str__(self):
        return make_response(jsonify(self.value), HTTPStatus.BAD_REQUEST)
