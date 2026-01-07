from pathlib import Path
from aiohttp import ClientTimeout

# Base Dir
BASE_DIR = Path(__file__).resolve().parent.parent

# Настройки Подключения / Settings
AIOHTTP_TIMEOUT = ClientTimeout(
    total=5,
    connect=2,
    sock_read=3,
)
MAX_RETRIES = 3

# Currency API Settings
CURRENCY_API_URL = "https://api.frankfurter.app/latest"
BASE_CURRENCY = "USD"
SUPPORTED_CURRENCIES: tuple[str, ...] = ("EUR", "GBP", "UAH")

# Ключи параметров для запросов / Key parameters for requests
CURRENCY_PARAM_FROM = 'from'
CURRENCY_PARAM_TO = 'to'

# Crypto API Settings
CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
CRYPTO_VS_CURRENCY = 'usd'

# MAPPING
CRYPTO_MAPPING: dict[str, str] = {
    "BTC": 'bitcoin',
    "ETH": "ethereum",
    "DOGE": "dogecoin",
}

def get_crypto_ids(mapping: dict[str, str]) -> str:
    if not mapping:
        raise ValueError("CRYPTO_MAPPING is empty")
    return ",".join(mapping.values())

CRYPTO_IDS = get_crypto_ids(CRYPTO_MAPPING)

# Key
CRYPTO_PARAM_IDS = 'ids'
CRYPTO_PARAM_VS = "vs_currencies"

# Cache Settings
MAX_AGE_MINUTES = 30
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
PATH_TO_CACHE = BASE_DIR / "data/rates.json"
ENCODING = "utf-8"
DATE_FORMAT_FOR_FILE = "%Y%m%d_%H%M%S"

# Cache Key
CACHE_KEY_TIMESTAMP = 'timestamp'
CACHE_KEY_DATA = 'data'

# Report Key
CUR_KEY = 'currency'
CRY_KEY = 'crypto'

# Log Settings
LOG_FORMAT = (
    '%(asctime)s | %(levelname)s | '
    '%(name)s | %(source)s | %(message)s'
)
LOG_PATH = BASE_DIR / "data/logs/app.log"
LOGGER_NAME = "currency_api"
LOG_MAX_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 5

EMPTY_CACHE = {}