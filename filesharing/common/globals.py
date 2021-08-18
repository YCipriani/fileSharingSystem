from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from filesharing.common.read_credentials import get_all_credentials

credentials = get_all_credentials()
scheduler = BackgroundScheduler()
dummy_file = {"file_name": "dummy_file", "file_location": None}
extensions = [".exe", ".txt", ".doc", ".pdf"]
