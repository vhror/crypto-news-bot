import argparse
import threading
from scheduler import schedule_jobs_test_every_min, schedule_jobs_production, run_loop
from bot import bot


def start_scheduler(test=False):
    if test:
        schedule_jobs_test_every_min()
    else:
        schedule_jobs_production()
    run_loop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='Run scheduler in test mode (every minute)')
    args = parser.parse_args()

    # 1️⃣ Scheduler uchun thread
    t = threading.Thread(target=start_scheduler, args=(args.test,))
    t.start()

    # 2️⃣ Bot polling asosiy oqimda
    print("🤖 Bot polling started...")
    bot.infinity_polling()


if __name__ == '__main__':
    main()

