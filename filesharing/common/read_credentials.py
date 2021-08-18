import json
from filesharing.common.logger import get_logger
from filesharing.utils.current_time import print_date_time


def get_all_credentials():
    log = get_logger()
    f = open(
        "/Users/yonatancipriani/PycharmProjects/fileSharing/filesharing/resources/credentials.json"
    )
    data = json.load(f)
    if data:
        log.info(print_date_time() + "All credentials have been retrieved")
        return data
    else:
        log.info(print_date_time() + "No credentials found")
