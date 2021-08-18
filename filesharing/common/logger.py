import logging
from colorlog import ColoredFormatter

from os.path import dirname


def get_logger():
    logging.basicConfig(filename=dirname(dirname(__file__)) + "/logs/demo.log")
    LOG_LEVEL = logging.DEBUG
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
