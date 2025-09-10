import schedule
import time
from datetime import datetime
from config import SCHEDULE
from services.news import fetch_latest_news, format_news_caption
from services.prices import fetch_prices, format_price_text
from bot import send_price_post, send_news_post, send_error_to_dev


def job_send_prices():
    try:
        data = fetch_prices()
        caption = format_price_text(data)
        send_price_post(caption)
        print(f"[{datetime.now()}] Sent price post")
        send_error_to_dev(f"[{datetime.now()}] ✅ Price post sent")
    except Exception as e:
        print("Error in job_send_prices:", e)
        send_error_to_dev(f"❌ Error in job_send_prices:\n{e}")


def job_send_news():
    try:
        items = fetch_latest_news()
        if not items:
            print("No news items found")
            return
        caption = format_news_caption(items)
        image = items[0].get('image')
        send_news_post(image, caption)
        print(f"[{datetime.now()}] Sent news post")
        send_error_to_dev(f"[{datetime.now()}] ✅ News post sent")
    except Exception as e:
        print("Error in job_send_news:", e)
        send_error_to_dev(f"❌ Error in job_send_news:\n{e}")


def schedule_jobs_test_every_min():
    schedule.every(1).minutes.do(job_send_prices)
    schedule.every(1).minutes.do(job_send_news)


def schedule_jobs_production():
    for t in SCHEDULE.get('prices', []):
        schedule.every().day.at(t).do(job_send_prices)
    for t in SCHEDULE.get('news', []):
        schedule.every().day.at(t).do(job_send_news)


def run_loop():
    print("Scheduler loop started")
    send_error_to_dev("Scheduler loop started")
    while True:
        schedule.run_pending()
        time.sleep(1)
