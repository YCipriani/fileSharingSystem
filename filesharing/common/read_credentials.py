import json
import jsonify
from filesharing.common.logger import get_logger

log = get_logger()


def get_all_credentials():
    f = open(
        "/Users/yonatancipriani/PycharmProjects/fileSharing/filesharing/resources/credentials.json"
    )
    data = json.load(f)
    if data:
        log.info(" All credentials have been retrieved")
        return data
    else:
        log.info(" No credentials found")
