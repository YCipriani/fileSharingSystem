from apscheduler.schedulers.background import BackgroundScheduler
from filesharing.common.read_credentials import get_all_credentials

credentials = get_all_credentials()
scheduler = BackgroundScheduler()
extensions = [".exe", ".txt", ".doc", ".pdf"]
