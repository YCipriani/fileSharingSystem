import os
import json
import requests
from simplexml import dumps
from flask import Flask, make_response, jsonify, request
from flask_restful import Api
from filesharing.common.globals import scheduler
from filesharing.screens import login
from filesharing.utils.current_time import print_date_time
from filesharing.utils.notifications import send_email
from filesharing.domains.request import Request
import time
import atexit
from filesharing.common.logger import get_logger

flask_app = Flask(__name__)
flask_app.use_reloader = False

api = Api(flask_app)
admin_email = "yonatancipriani@outlook.com"


@flask_app.route("/", methods=["GET"])
def home():
    return """<h1>Flask App is Running</h1>"""


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@flask_app.route("/shutdown", methods=["GET"])
def shutdown():
    atexit.register(lambda: scheduler.shutdown())
    shutdown_server()
    return "Server shutting down..."


@api.representation("application/json")
def output_json(data, code, headers=None):
    resp = make_response(json.dumps({"response": data}), code)
    resp.headers.extend(headers or {})
    return resp


@api.representation("application/xml")
def output_xml(data, code, headers=None):
    resp = make_response(dumps({"response": data}), code)
    resp.headers.extend(headers or {})
    return resp


def start_app():
    flask_app.run()


def main():
    log = get_logger()
    request_type = input("For a Rx request press 0, for a Tx request press 1:\t")
    file_name_and_extension = input("Enter the file name including its extension:\t")
    file_location = input("Enter the file location:\t")
    if int(request_type) == 1:
        time_interval = input("Enter the time interval between requests in seconds:\t")
        request_test = Request(
            request_type="Tx",
            file_name_and_extension=file_name_and_extension,
            file_location=file_location,
            time=int(time_interval),
        )
        # send_email("Tx", file_name_and_extension, file_location, admin_email)
    else:
        while True:
            number_of_checks = input(
                "Enter the number of checks (respond only with numbers no letters):\t"
            )
            try:
                n = int(number_of_checks)
                break
            except ValueError:
                log.error(print_date_time() + "User entered text instead of only digits")
                print("ERROR: Only NUMBERS are allowed")
                c = input("Do you want to try again? (y/n)")
                if c == "y":
                    continue
                else:
                    exit(0)

        request_test = Request(
            request_type="Rx",
            file_name_and_extension=file_name_and_extension,
            file_location=file_location,
            number_of_checks=n,
        )
        # send_email("Rx", file_name_and_extension, file_location, admin_email)

    login.login(request_test)


if __name__ == "__main__":
    main()
