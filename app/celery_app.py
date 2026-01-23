from celery import Celery

app = Celery(
    "derbit_worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

app.conf.worker_pool = "solo"
app.conf.worker_concurrency = 1
app.conf.task_acks_late = False

app.autodiscover_tasks(["app.worker"])

app.conf.beat_schedule = {
    "fetch_prices_every_minute": {
        "task": "app.worker.tasks.fetch_prices",
        "schedule": 60.0,
    }
}

app.conf.timezone = "UTC"
