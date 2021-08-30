import json
import os
import sys

from filesharing.common.logger import get_logger
from filesharing.utils.current_time import get_current_date_and_time

credentials_file_path = sys.path[0].replace("common", "").replace("/base_library.zip", "") + "/resources/credentials.json"


def get_all_credentials():
    log = get_logger()
    f = open(
        credentials_file_path
    )
    data = json.load(f)
    if data:
        return data
    else:
        log.info(get_current_date_and_time() + "No credentials found")
