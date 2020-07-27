import atexit

from apscheduler.schedulers.blocking import BlockingScheduler
from service.save_data_to_db import refresh_data




sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=10)
def timed_job():
    print('Refresh data from GOV Start')
    refresh_data()
    print('Refresh data from GOV End')


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())