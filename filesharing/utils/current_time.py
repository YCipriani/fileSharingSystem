import datetime
from random import randint


def service_started_time():
    file = open(
        "/Users/yonatancipriani/PycharmProjects/fileSharing/filesharing/resources/service_started_time.txt",
        "r",
    )
    lines = file.read().splitlines()
    return lines[-1]


def write_service_started_time_to_file(time):
    file = open(
        "/Users/yonatancipriani/PycharmProjects/fileSharing/filesharing/resources/service_started_time.txt",
        "w",
    )
    file.write(time)


def get_seconds_diff(time_interval):
    start = service_started_time()
    now = datetime.datetime.now()  # current date and time
    end = now.strftime("%Y-%m-%d %H:%M:%S")

    date1_obj = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    date2_obj = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')

    difference_seconds = abs((date1_obj - date2_obj).seconds)
    return time_interval - (difference_seconds % time_interval)


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
