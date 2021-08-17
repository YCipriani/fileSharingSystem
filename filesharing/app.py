import os
import json
import requests
from simplexml import dumps
from flask import Flask, make_response, jsonify, request
from flask_restful import Api
from filesharing.common.logger import get_logger
from filesharing.screens import login
from filesharing.utils.notifications import send_email
from filesharing.domains.request import Request
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


flask_app = Flask(__name__)
flask_app.use_reloader = False

api = Api(flask_app)
admin_email = "yonatancipriani@outlook.com"


# api = Api(app, default_mediatype='application/json')

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


# api.representations['application/json'] = output_json
# api.representations['application/xml'] = output_xml
def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


def start_app():
    flask_app.run()


def main():
    # request_type = input("For a Rx request press 0, for a Tx request press 1:\t")
    # file_name_and_extension = input("Enter the file name including its extension:\t")
    # file_location = input("Enter the file location (table/collection) where you want the file to be stored:\t")
    # if request_type:
    #     time_interval = input("Enter the time interval between requests in seconds:\t")
    #     request = Request(file_name_and_extension=file_name_and_extension, file_location=file_location, time=time_interval)
    #     send_email("Tx", file_name_and_extension, file_location, admin_email)
    # else:
    #     number_of_checks = input("Enter the number of checks:")
    #     request = Request(file_name_and_extension=file_name_and_extension, file_location=file_location, number_of_checks=number_of_checks)
    #     send_email("Rx", file_name_and_extension, file_location, admin_email)
    # api.add_resource(rest.Greet, '/')
    # api.add_resource(rest.GreetName, '/<string:name>')
    # send_email("Tx", "sample.txt", "yonatancipriani@outlook.com")

    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
    # scheduler.start()
    login.login()
    start_app()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    main()
