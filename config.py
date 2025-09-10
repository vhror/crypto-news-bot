import json
from pathlib import Path
import os

CHANNELS_FILE = Path(__file__).parent / "channels.json"


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_IDS = "@crypto_news_dally"
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/crypto_news_dally")

DEVELOPER_ID = int(os.getenv("DEVELOPER_ID")) if os.getenv("DEVELOPER_ID") else None

COINS = [
    "bitcoin", "ethereum", "tether", "binancecoin",
    "solana", "ripple", "usd-coin", "cardano",
    "dogecoin", "avalanche-2", "the-open-network"
]

SCHEDULE = {
    'prices': ["09:00", "15:00", "21:00"],
    'news': ["12:00", "20:00"]


}

NEWS_PER_POST = 6

COINGECKO_SIMPLE_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price"

RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/"
]

def load_channels():
    if CHANNELS_FILE.exists():
        with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("channels", [])
    return []

def save_channels(channels):
    with open(CHANNELS_FILE, "w", encoding="utf-8") as f:
        json.dump({"channels": channels}, f, indent=4)

CHANNEL_IDS = load_channels()