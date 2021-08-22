import json
import time

from bson import json_util
from simplexml import dumps
from flask import Flask, make_response, request
from flask_restful import Api
from filesharing.db.mongodbDAL import mongodbDAL
from filesharing.screens import login
from filesharing.utils.current_time import get_current_date_and_time, create_dummy_file, get_seconds_diff
from filesharing.utils.notifications import send_email
from filesharing.domains.request import Request
import socket
from contextlib import closing
from filesharing.common.logger import get_logger
from filesharing.utils.port import write_port_to_file, read_port_from_file

flask_app = Flask(__name__)
flask_app.use_reloader = False

api = Api(flask_app)
admin_email = "yonatancipriani@outlook.com"


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


@flask_app.route("/", methods=["GET"])
def home():
    return """<h1>Service is Running</h1>"""


@flask_app.route("/send_request", methods=["POST"])
def send_request():
    log = get_logger()
    if len(request.args.to_dict()) == 3:
        request_type = request.args.get("request_type")
        file_name = request.args.get("file_name")
        file_location = request.args.get("file_location")
    else:
        if len(request.json) == 3:
            request_type = request.json["request_type"]
            file_name = request.json["file_name"]
            file_location = request.json["file_location"]
        else:
            log.error(
                "Not all of the arguments were provided (request_type, file_name, file_location"
            )
            return "Not all of the arguments were provided (request_type, file_name, file_location"
    file = {
        "file_name": file_name,
        "file_location": file_location,
    }
    dal = mongodbDAL(request_type)
    collection = dal.db.get_collection(file_location)
    if request_type == "Tx":
        rx_dal = mongodbDAL("Rx")
        rx_collection = rx_dal.db.get_collection(file_location)
        dummy_file = create_dummy_file(file_location)
        collection.insert_one(dummy_file)
        rx_collection.insert_one(dummy_file)
        log.info(
            get_current_date_and_time()
            + "Dummy file "
            + dummy_file["file_name"]
            + " was stored in collection"
            + dummy_file["file_location"]
            + "."
        )
        if not dal.find_file_by_collection(file_name, file_location):
            collection.insert_one(file)
            rx_collection.insert_one(file)
            log.info(
                get_current_date_and_time()
                + "File "
                + file_name
                + " was stored in collection "
                + file_location
                + "."
            )
            return json.loads(json_util.dumps(file))
        log.error(
            get_current_date_and_time()
            + "File "
            + file_name
            + " already exists in collection "
            + file_location
            + "."
        )
        return "File is already in the collection/table"
    if request_type == "Rx":
        tx_dal = mongodbDAL("Tx")
        if dal.find_file_by_collection(
            file_name, file_location
        ) and tx_dal.find_file_by_collection(file_name, file_location):
            print("File " + file_name + " was found")
            return (
                "File " + file_name + " was found in collection " + file_location + "."
            )
        else:
            log.error(
                get_current_date_and_time()
                + "File "
                + file_name
                + " was NOT found in collection "
                + file_location
                + "."
            )
            print(
                "File "
                + file_name
                + " was NOT found in collection "
                + file_location
                + "."
            )
            return None


@flask_app.route("/send_tx_request", methods=["POST"])
def send_the_tx_request():
    log = get_logger()
    if len(request.args.to_dict()) == 3:
        file_name = request.args.get("file_name")
        file_location = request.args.get("file_location")
        time_interval = request.args.get("time_interval")
    else:
        if len(request.json) == 3:
            time_interval = request.json["time_interval"]
            file_name = request.json["file_name"]
            file_location = request.json["file_location"]
        else:
            log.error(
                "Not all of the arguments were provided (request_type, file_name, file_location"
            )
            return "Not all of the arguments were provided (request_type, file_name, file_location"
    file = {
        "file_name": file_name,
        "file_location": file_location,
    }
    dal = mongodbDAL("Tx")
    collection = dal.db.get_collection(file_location)
    rx_dal = mongodbDAL("Rx")
    rx_collection = rx_dal.db.get_collection(file_location)
    time.sleep(get_seconds_diff(int(time_interval)))
    if not dal.find_file_by_collection(file_name, file_location):
        collection.insert_one(file)
        rx_collection.insert_one(file)
        log.info(
            get_current_date_and_time()
            + "File "
            + file_name
            + " was stored in collection "
            + file_location
            + "."
        )
        return json.loads(json_util.dumps(file))
    log.error(
        get_current_date_and_time()
        + "File "
        + file_name
        + " already exists in collection "
        + file_location
        + "."
    )
    return "File is already in the collection/table"


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@flask_app.route("/new_request", methods=["GET"])
def new_request():
    log = get_logger()
    port = read_port_from_file()
    try:
        shutdown_server()
        start_app(port)
    except:
        new_port = find_free_port()
        write_port_to_file(new_port)
        log.info("New server starting at port number: " + str(new_port))
        start_app(port=new_port)
    return "Restarted the Service on Port " + str(port)


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


def start_app(port=5000):
    write_port_to_file(port)
    flask_app.run(port=port)


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
    elif int(request_type) == 0:
        n = 0
        while True:
            number_of_checks = input(
                "Enter the number of checks (respond only with numbers no letters):\t"
            )
            try:
                n = int(number_of_checks)
                break
            except ValueError:
                log.error(
                    get_current_date_and_time()
                    + "User entered text instead of only digits"
                )
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
    else:
        log.error(
            get_current_date_and_time()
            + "Only Tx (press 1) and Rx (press 0) requests are allowed"
        )
        return "Only Tx (press 1) and Rx (press 0) requests are allowed"

    login.login(request_test)


if __name__ == "__main__":
    main()
