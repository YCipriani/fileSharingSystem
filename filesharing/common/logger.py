import logging
from colorlog import ColoredFormatter
import os

log_file_path = os.path.dirname(os.path.abspath(__file__)).replace("common", "") + "logs/demo.log"

def get_logger():
    logging.basicConfig(filename=log_file_path)
    LOG_LEVEL = logging.INFO
    LOGFORMAT = (
        "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
    )
    logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(LOGFORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    log = logging.getLogger()
    log.setLevel(LOG_LEVEL)
    log.addHandler(stream)
    return log
