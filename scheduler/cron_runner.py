from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pipelines.biweekly_narrative_run import run_pipeline
from config.settings import settings
import logging
logging.basicConfig(level=logging.INFO)
scheduler = BlockingScheduler()
scheduler.add_job(run_pipeline, IntervalTrigger(days=settings.run_cadence_days), id="narrative_pipeline", replace_existing=True)
if __name__ == "__main__":
    scheduler.start()
