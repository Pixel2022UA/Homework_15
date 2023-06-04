import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchange_rates.settings")

app = Celery("exchange_rates")
every_3_am = crontab(minute=0, hour=3)  # crontab(minute='*/5')
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "mono-USD-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": every_3_am,
        "args": ("mono", "USD", "UAH"),
    },
    "mono-EUR-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": every_3_am,
        "args": ("mono", "EUR", "UAH"),
    },
    "privat-EUR-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": every_3_am,
        "args": ("privat", "EUR", "UAH"),
    },
    "privat-USD-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": every_3_am,
        "args": ("privat", "USD", "UAH"),
    },
    "nacbank-USD-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": every_3_am,
        "args": ("nacbank", "USD", "UAH"),
    },
    "nacbank-EUR-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": every_3_am,
        "args": ("nacbank", "EUR", "UAH"),
    },
    "openexch-EUR-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": every_3_am,
        "args": ("openexch", "USD", "UAH"),
    },
    "layer-USD-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": every_3_am,
        "args": ("layer", "USD", "UAH"),
    },
}
