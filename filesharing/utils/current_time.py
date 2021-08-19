from datetime import datetime
from random import randint


def get_current_date_and_time():
    return datetime.today().strftime(" %Y-%m-%d %H:%M:%S ")


def create_dummy_file(collection_name):
    dummy_file = {
        "file_name": (
            str(randint(0, 8883342)) + get_current_date_and_time() + ".txt"
        ).replace(" ", "_"),
        "file_location": collection_name,
    }
    return dummy_file
