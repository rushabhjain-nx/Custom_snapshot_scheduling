from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from .schedular import start_scheduler
        logger.info("Starting scheduler...")
        start_scheduler()
        logger.info("Scheduler started.")
