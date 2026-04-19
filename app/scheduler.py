from apscheduler.schedulers.blocking import BlockingScheduler


def start_scheduler(job_func, timezone: str) -> None:
    scheduler = BlockingScheduler(timezone=timezone)
    
    scheduler.add_job(job_func, "cron", hour=23, minute=58)

    print("Scheduler started.")
    scheduler.start()