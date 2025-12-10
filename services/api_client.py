import aiohttp
import asyncio
import app_config
from utils import Validators, AppLogger
from models_p2 import RatesReport

logger = AppLogger.get_logger(__name__)

class ApiError(Exception):
    pass


class ApiClient:
    """
    Клиент для взаимодействия с внешними API курсов валют и криптовалют.
    Реализует механизм повторных попыток (retry) и единую сессию aiohttp.
    """

    def __init__(self):
        self.validators = Validators()

    @staticmethod
    async def _perform_request(session: aiohttp.ClientSession, url: str, params=None):
        """
        Выполняет одиночный HTTP GET-запрос с тайм-аутом.
        Статический метод, так как не зависит от состояния экземпляра класса.
        """
        async with asyncio.timeout(app_config.DEFAULT_TIMEOUT):
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise ApiError(f"Ошибка API: HTTP {response.status}")
                return await response.json()

    async def fetch_json(self, session: aiohttp.ClientSession, url: str, params=None):
        """Оркестратор повторных попыток."""
        last_error = None

        for attempt in range(app_config.MAX_RETRIES):
            try:
                # Пытаемся выполнить запрос
                return await self._perform_request(session, url, params)
            except (aiohttp.ClientError, asyncio.TimeoutError, ApiError) as e:
                # Если ошибка - делегируем обработку
                last_error = e
                await self._handle_retry_error(e, attempt)

        logger.error(f"API полностью недоступно: {last_error}")
        raise last_error

    @staticmethod
    async def _handle_retry_error(error: Exception, attempt: int):
        """Вспомогательный метод: логгирует ошибку и ждет перед следующей попыткой."""
        logger.warning(f"Попытка {attempt + 1}/{app_config.MAX_RETRIES} не удалась: {error}")

        if attempt < app_config.MAX_RETRIES -1:
            await asyncio.sleep(1)


    async def fetch_currency_rates(self, session: aiohttp.ClientSession):
        """Получает курсы фиатных валют (EUR, GBP, etc)."""
        params = {
            app_config.CURRENCY_PARAM_FROM: app_config.BASE_CURRENCY,
            app_config.CURRENCY_PARAM_TO: app_config.SUPPORTED_CURRENCIES
        }

        data = await  self.fetch_json(session, app_config.CURRENCY_API_URL, params=params)
        rates = data.get("rates", {})

        self.validators.check_empty_currency(rates)
        return rates

    async def fetch_crypto_rates(self, session: aiohttp.ClientSession):
        """Получает курсы криптовалют и приводит их к удобному формату."""
        params = {
            app_config.CRYPTO_PARAM_IDS: app_config.CRYPTO_IDS,
            app_config.CRYPTO_PARAM_VS: app_config.CRYPTO_VS_CURRENCY
        }

        data = await self.fetch_json(session, app_config.CRYPTO_API_URL, params=params)

        # Пересобираем словарь, используя маппинг из конфига
        return {
            short_name: data.get(api_id, {}).get(app_config.CRYPTO_VS_CURRENCY)
            for short_name, api_id in app_config.CRYPTO_MAPPING.items()
        }

    async def fetch_all(self):
        """
        Основной метод входа.
        Создает единую сессию aiohttp и запускает параллельный сбор всех данных.
        """
        async with aiohttp.ClientSession() as session:
            # Запускаем задачи, передавая им одну и ту же сессию
            currency_task = asyncio.create_task(self.fetch_currency_rates(session))
            crypto_task = asyncio.create_task(self.fetch_crypto_rates(session))

            # Дожидаемся завершения всех задач
            currency, crypto = await asyncio.gather(currency_task, crypto_task)

            return RatesReport(currency, crypto)
