import os
import json
import requests
from simplexml import dumps
from flask import Flask, make_response, jsonify, request
from flask_restful import Api
from filesharing.common.logger import get_logger
from filesharing.utils.notifications import send_email
from filesharing.domains.request import Request



app = Flask(__name__)

api = Api(app)


# api = Api(app, default_mediatype='application/json')

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Flask App is Running</h1>'''

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps({'response': data}), code)
    resp.headers.extend(headers or {})
    return resp


@api.representation('application/xml')
def output_xml(data, code, headers=None):
    resp = make_response(dumps({'response': data}), code)
    resp.headers.extend(headers or {})
    return resp

# api.representations['application/json'] = output_json
# api.representations['application/xml'] = output_xml

def start_app():
    app.run()

def shutdown_server():
    import sys
    sys.exit()

def main():
    request_type = input("For a Rx request press 0 and for a Tx request press 1:\t")
    file_name_and_extension = input("Enter the file name and its extension:\t")
    file_location = input("Enter the file location where it will be stored:\t")
    if request_type:
        time_interval = input("Enter the time interval between requests in seconds:\t")
        request = Request(file_name_and_extension=file_name_and_extension, file_location=file_location, time=time_interval)
        # send_email("Tx", file_name_and_extension, file_location, email)
    else:
        number_of_checks = input("Enter the number of checks:")
        request = Request(file_name_and_extension=file_name_and_extension, file_location=file_location, number_of_checks=number_of_checks)
        # send_email("Rx", file_name_and_extension, file_location, email)
    # api.add_resource(rest.Greet, '/')
    # api.add_resource(rest.GreetName, '/<string:name>')
    # send_email("Tx", "sample.txt", "yonatancipriani@outlook.com")
    start_app()
    import time
    time.sleep(5)
    shutdown_server()


if __name__ == "__main__":
    main()
