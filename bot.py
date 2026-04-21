
import requests
import time
import os
from datetime import datetime

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

symbol = "BTCUSDT"
interval = "1m"

last_candle_time = None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def get_latest_candle():
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=1"
    response = requests.get(url).json()

    candle = response[0]
    candle_open_time = candle[0]
    volume = float(candle[5])

    return candle_open_time, volume

while True:
    try:
        candle_time, volume = get_latest_candle()

        if candle_time != last_candle_time:
            last_candle_time = candle_time

            day = datetime.utcnow().weekday()

            if day >= 5:
                threshold = 400
            else:
                threshold = 850

            if volume >= threshold:
                send_telegram(
                    f"🚨 Volume Alert\n"
                    f"Pair: {symbol}\n"
                    f"Volume: {volume}\n"
                    f"Threshold: {threshold}"
                )

        time.sleep(60)

    except Exception as e:
        send_telegram(f"Bot Error: {str(e)}")
        time.sleep(60)
