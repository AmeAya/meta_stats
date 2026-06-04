from celery import shared_task
from celery_once import QueueOnce
from datetime import date, timedelta

from .functions import get_fb_insights


@shared_task(base=QueueOnce, once={"graceful": True}, ignore_result=True)
def fetch_fb_insights():
    ad_account_ids = ["act_1341554981006249", "act_727300020106328"]
    for ad_account_id in ad_account_ids:
        for i in range(7):
            day = date.today() - timedelta(days=i + 1)
            since = str(day)
            until = str(day)
            get_fb_insights(since, until, ad_account_id)
