import requests
from config import COINS, COINGECKO_SIMPLE_PRICE_URL, CHANNEL_LINK


def fetch_prices():
    params = {
        "ids": ",".join(COINS),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    resp = requests.get(COINGECKO_SIMPLE_PRICE_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def format_price_text(prices_json):
    lines = ["📊 <b>Crypto Prices 💵 (USD)</b>\n"]
    for coin in COINS:
        data = prices_json.get(coin, {})
        price = data.get('usd')
        change = data.get('usd_24h_change')
        if price is None or change is None:
            continue

        # format price
        if price >= 1:
            price_str = f"${price:,.2f}"
        else:
            price_str = f"${price:.8f}"

        # sign + arrow
        sign = '+' if change >= 0 else ''
        arrow = '📈' if change >= 0 else '📉'
        change_str = f"{sign}{change:.2f}%"

        # separate lines for clarity
        lines.append(f"<b>{coin.upper()}</b>: {price_str}")
        lines.append(f"{arrow} <i>{change_str}</i>\n")

    lines.append("#crypto #bitcoin #ethereum #altcoins")
    lines.append(f"\n<a href='{CHANNEL_LINK}'>Crypto News Daily</a>")
    return "\n".join(lines)
