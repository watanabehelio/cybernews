from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

def job():
    from ingest.rss_ingestor import run as run_rss
    run_rss()

scheduler = BackgroundScheduler(timezone=pytz.timezone("America/Sao_Paulo"))

def start_scheduler(app):
    scheduler.add_job(job, CronTrigger(hour=7, minute=0))
    scheduler.start()

    @app.on_event("shutdown")
    def shutdown_event():
        scheduler.shutdown()
