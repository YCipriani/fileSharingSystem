import datetime
import json
from random import randint
import os
import sys

service_started_file_path = sys.path[0].replace("utils", "").replace("/base_library.zip", "") + "/resources/service_started_time.json"
number_of_checks_file_path = sys.path[0].replace("utils", "").replace("/base_library.zip", "") + "/resources/number_of_checks.txt"


def service_started_time():
    with open(
        service_started_file_path
    ) as f:
        return json.load(f)


def write_service_started_time_to_file(time, flag):
    if flag:
        jsonData = {"started": True, "started_time": time}
    else:
        jsonData = {"started": False, "started_time": time}
    with open(
        service_started_file_path,
        "w",
    ) as outfile:
        json.dump(jsonData, outfile, sort_keys=True, indent=4, ensure_ascii=False)


def get_seconds_diff(time_interval):
    d = service_started_time()
    start = d["started_time"]
    now = datetime.datetime.now()  # current date and time
    end = now.strftime("%Y-%m-%d %H:%M:%S")

    date1_obj = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    date2_obj = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")

    difference_seconds = abs((date1_obj - date2_obj).seconds)
    return time_interval - (difference_seconds % time_interval)


def number_of_checks_made():
    file = open(
        number_of_checks_file_path,
        "r",
    )
    lines = file.read().splitlines()
    return lines[-1]


def write_number_of_checks_made(n):
    file = open(
        number_of_checks_file_path,
        "w",
    )
    file.write(str(n))


def get_current_date_and_time():
    return datetime.datetime.today().strftime(" %Y-%m-%d %H:%M:%S ")


def create_dummy_file(collection_name):
    dummy_file = {
        "file_name": (
            str(randint(0, 8883342)) + get_current_date_and_time() + ".txt"
        ).replace(" ", "_"),
        "file_location": collection_name,
    }
    return dummy_file
