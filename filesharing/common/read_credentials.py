import json
from filesharing.common.logger import get_logger
from filesharing.utils.current_time import get_current_date_and_time


def get_all_credentials():
    log = get_logger()
    f = open(
        "/Users/yonatancipriani/PycharmProjects/fileSharing/filesharing/resources/credentials.json"
    )
    data = json.load(f)
    if data:
        return data
    else:
        log.info(get_current_date_and_time() + "No credentials found")
