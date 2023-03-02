"""Initialize any app extensions."""


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.triggers.cron import CronTrigger
from config import client

jobstore = MongoDBJobStore(client=client)
scheduler = BackgroundScheduler()
scheduler.add_jobstore(jobstore)



trigger = CronTrigger(day_of_week='mon', hour=5)