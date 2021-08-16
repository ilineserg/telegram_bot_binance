import os


TA_API_TOKEN = os.environ.get('TA_API_TOKEN')
TLG_TOKEN = os.environ.get('TLG_TOKEN')

INDICATORS = ["macd", "rsi", "aroon", "stoch", "ultosc",]
SYMBOLS = ["BTC/USDT", ]
INTERVAL = "15m"
CHAT_ID = ""  # TODO: value

# indicators values
MACD_EXPECTED_VALUE = -35
RSI_EXPECTED_VALUE = 7
AROON_EXPECTED_VALUE = 7
STOCH_EXPECTED_VALUE = 20
ULTOSC_EXPECTED_VALUE = 0  # TODO: value
