import logging
from colorlog import ColoredFormatter


def get_logger():
    logging.basicConfig(filename="/Users/yonatancipriani/PycharmProjects/fileSharing/filesharing/logs/demo.log")
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
