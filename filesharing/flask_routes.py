from flask import request, jsonify
from flask_restful import Resource
import json
from filesharing.app import flask_app
from filesharing.common.logger import get_logger


class Greet(Resource):
    def get(self):
        return {"message": "Hello, how are you?"}

    def post(self):
        req = request.get_json()
        print("req", req)
        return req, 201


class GreetName(Resource):
    def get(self, name):
        return {"message": "Hello " + name + ", how are you?"}


class Credentials(Resource):
    def post(self):
        f = open(
            "credentials.json",
        )
        data = json.load(f)
        if data:
            return jsonify(data)
