import threading
import logging
import schedule
import time
from .views import check_ss

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Singleton pattern for scheduler
scheduler_instance = None
lock = threading.Lock()

def my_function():
    with lock:
        logger.info("Running snapshot check...")
        check_ss()
        logger.info("Snapshot check completed.")

def run_scheduler():
    schedule.every(1).minutes.do(my_function)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    global scheduler_instance
    if scheduler_instance is None:
        with lock:
            if scheduler_instance is None:  # Double-check inside lock
                scheduler_instance = threading.Thread(target=run_scheduler, name="SchedulerThread")
                scheduler_instance.daemon = True
                scheduler_instance.start()
                logger.info("Scheduler thread started.")
