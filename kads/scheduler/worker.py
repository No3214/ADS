import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from kads.scheduler.jobs import job_p0_health_check, job_p1_optimization, job_reflection
from kads.data.warehouse.db import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("kads.worker")

def start_worker(blocking: bool = True):
    logger.info("Initializing KADS Warehouse DB...")
    init_db()

    logger.info("Starting KADS Background Scheduler...")
    scheduler = BackgroundScheduler()

    # Schedule P0 health check every 15 minutes
    scheduler.add_job(job_p0_health_check, "interval", minutes=15, id="p0_health_check")
    
    # Schedule P1 optimization every 1 hour
    scheduler.add_job(job_p1_optimization, "interval", hours=1, id="p1_optimization")
    
    # Schedule reflection every day at 02:00
    scheduler.add_job(job_reflection, "cron", hour=2, minute=0, id="reflection")

    scheduler.start()
    logger.info("KADS Background Scheduler started successfully.")

    if not blocking:
        return scheduler

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler stopped.")
        return None

if __name__ == "__main__":
    start_worker()
