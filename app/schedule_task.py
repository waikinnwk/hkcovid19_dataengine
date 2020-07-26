import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from service.save_data_to_db import refresh_data



scheduler = BackgroundScheduler()
scheduler.add_job(func=refresh_data, trigger="interval", hours=2)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())