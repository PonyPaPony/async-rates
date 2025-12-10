# Настройки подключения
DEFAULT_TIMEOUT = 5
MAX_RETRIES = 3

# --- Currency API Settings ---
CURRENCY_API_URL = "https://api.frankfurter.app/latest"
BASE_CURRENCY = "USD"
SUPPORTED_CURRENCIES = "EUR,GBP,UAH"

# Ключи параметров для запроса (если API изменит названия параметров, меняем их здесь)
CURRENCY_PARAM_FROM = "from"
CURRENCY_PARAM_TO = "to"


# --- Crypto API Settings ---
CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
CRYPTO_VS_CURRENCY = "usd" # В какой валюте получать цену (lower case для API)

# Маппинг: Наше название -> ID в API
CRYPTO_MAPPING = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "DOGE": "dogecoin",
}

# Автоматически собираем строку ID для запроса
CRYPTO_IDS = ",".join(CRYPTO_MAPPING.values())

# Ключи параметров для запроса
CRYPTO_PARAM_IDS = "ids"
CRYPTO_PARAM_VS = "vs_currencies"

# --- Настройки кэширования ---
MAX_AGE_MINUTES = 30
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
PATH_TO_CACHE = "data/rates.json"
ENCODING = "utf-8"
DATE_FORMAT_FOR_FILE = "%Y%m%d_%H%M%S"

# Ключи внутренней структуры JSON-кэша
CACHE_KEY_TIMESTAMP = "timestamp"
CACHE_KEY_DATA = "data"

# Ключи для репорта
CUR_KEY = "currency"
CRY_KEY = "crypto"

# Настройки логгера
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_PATH = "data/logs/app.log"
LOG_ENCODING = 'utf-8'
