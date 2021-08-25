import json
from filesharing.common.logger import get_logger
from filesharing.utils.current_time import get_current_date_and_time
import os

credentials_file_path = os.path.dirname(os.path.abspath(__file__)).replace("common", "") + "resources/credentials.json"

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
