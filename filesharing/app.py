import json
import time

from bson import json_util
from simplexml import dumps
from flask import Flask, make_response, request
from flask_restful import Api
from filesharing.db.mongodbDAL import mongodbDAL
from filesharing.screens import login
from filesharing.utils.current_time import (
    get_current_date_and_time,
    create_dummy_file,
    get_seconds_diff,
)
from filesharing.domains.request import Request
from filesharing.common.logger import get_logger
from filesharing.utils.notifications import send_email
from filesharing.utils.port import (
    write_port_to_file,
    read_port_from_file,
    find_free_port,
)
from filesharing.common.globals import admin_email

flask_app = Flask(__name__)
flask_app.use_reloader = False

api = Api(flask_app)


@flask_app.route("/", methods=["GET"])
def home():
    return """<h1>Service is Running</h1>"""


@flask_app.route("/move_file", methods=["POST"])
def move_file():
    if len(request.args.to_dict()) == 3:
        file_name = request.args.get("file_name")
        old_location = request.args.get("old_location")
        new_location = request.args.get("new_location")
        try:
            tx_dal = mongodbDAL("Tx")
            rx_dal = mongodbDAL("Rx")
            tx_dal.move_file(file_name, old_location, new_location)
            rx_dal.move_file(file_name, old_location, new_location)
            return "File " + file_name + " was moved from collection " + old_location + " to collection " + new_location
        except:
            return "Could not preform operation. Make sure file is in the old location specified"
    return "Not enough parameters were passed"


# @flask_app.route("/clear_logs", methods=["POST"])
# def clear_logs():
#     open("/Users/yonatancipriani/PycharmProjects/fileSharing/filesharing/logs/demo.log", "w").close()
#     return "Logs have been cleared"


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
            + " was stored in collection "
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
            return "SUCCESS"
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
            return "SUCCESS"
        else:
            log.error(
                get_current_date_and_time()
                + "File "
                + file_name
                + " was NOT found in collection "
                + file_location
                + "."
            )
            return "File " + file_name + " was NOT found in collection " + file_location + "."


@flask_app.route("/send_rx_request", methods=["POST"])
def send_the_rx_request():
    log = get_logger()
    if len(request.args.to_dict()) == 3:
        file_name = request.args.get("file_name")
        file_location = request.args.get("file_location")
        number_of_checks = request.args.get("number_of_checks")
    else:
        if len(request.json) == 3:
            number_of_checks = request.json["number_of_checks"]
            file_name = request.json["file_name"]
            file_location = request.json["file_location"]
        else:
            log.error(
                "Not all of the arguments were provided (request_type, file_name, file_location)"
            )
            return "Not all of the arguments were provided (request_type, file_name, file_location)"
    tx_dal = mongodbDAL("Tx")
    rx_dal = mongodbDAL("Rx")
    count = 0
    try:
        n = int(number_of_checks)
    except:
        log.error(get_current_date_and_time() + "ERROR: number_of_checks is not a number")
        return "ERROR: number_of_checks is not a number"
    my_request = Request(
        request_type="Rx",
        file_name_and_extension=file_name,
        file_location=file_location,
        number_of_checks=n,
    )
    send_email(my_request, admin_email, True)
    for i in range(n):
        if rx_dal.find_file_by_collection(
                file_name, file_location
        ) and tx_dal.find_file_by_collection(file_name, file_location):
            count += 1
    send_email(my_request, admin_email, False)
    if n != count:
        log.info(get_current_date_and_time() + "File " + file_name + " was NOT found in collection " + file_location + ".")
        return "File " + file_name + " was NOT found in collection " + file_location + "."
    else:
        log.error(get_current_date_and_time() + "File " + file_name + " was found in collection " + file_location + " " + number_of_checks + " times.")
        return "File " + file_name + " was found in collection " + file_location + " " + number_of_checks + " times."


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
                "Not all of the arguments were provided (request_type, file_name, file_location)"
            )
            return "Not all of the arguments were provided (request_type, file_name, file_location)"
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
        log.info(
            get_current_date_and_time()
            + "New server starting at port number: "
            + str(new_port)
        )
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
        request = Request(
            request_type="Tx",
            file_name_and_extension=file_name_and_extension,
            file_location=file_location,
            time=int(time_interval),
        )
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

        request = Request(
            request_type="Rx",
            file_name_and_extension=file_name_and_extension,
            file_location=file_location,
            number_of_checks=n,
        )
    else:
        log.error(
            get_current_date_and_time()
            + "Only Tx (press 1) and Rx (press 0) requests are allowed"
        )
        return "Only Tx (press 1) and Rx (press 0) requests are allowed"

    login.login(request)


if __name__ == "__main__":
    main()
