from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
dummy_file = {
    "file_name": "dummy_file",
    "file_location": None
}
extensions = [".exe", ".txt", ".doc"]