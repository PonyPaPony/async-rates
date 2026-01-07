import aiohttp
import asyncio
import random
import json

from typing import Dict, Any
from AsyncRates import app_config
from AsyncRates.utils.validators import Validators
from AsyncRates.utils.app_exceptions import ApiError
from AsyncRates.utils.logger import AppLogger
from AsyncRates.app_models.reports import RatesReport

logger = AppLogger.get_logger(__name__)


class ApiClient:
    def __init__(self):
        self.validators = Validators()

    @staticmethod
    async def _perform_request(
            session: aiohttp.ClientSession, url: str, params=None
    ) -> Dict[str, Any]:
        try:
            async with (session.get(
                    url,
                    timeout=app_config.AIOHTTP_TIMEOUT,
                    params=params)
            as response):
                body = await response.text()

                try:
                    response.raise_for_status()
                except aiohttp.ClientResponseError as e:
                    raise ApiError(
                        status=response.status,
                        message=f"API error {response.status}",
                        payload=body,
                        retryable=response.status >= 500,
                    ) from e

                try:
                    return await response.json(content_type=None)
                except (json.JSONDecodeError, aiohttp.ContentTypeError) as e:
                    raise ApiError(
                        status=response.status,
                        message="Response is not valid JSON",
                        payload=body,
                    ) from e

        except asyncio.TimeoutError as e:
            raise ApiError(
                status=None,
                message="Превышено время ожидания API",
                retryable=True,
            ) from e

        except aiohttp.ClientError as e:
            raise ApiError(
                status=None,
                message="Ошибка соединения с API",
                retryable=True,
            ) from e

    async def fetch_json(
            self,
            session: aiohttp.ClientSession,
            url: str,
            params=None
    ):
        last_error = None

        for attempt in range(app_config.MAX_RETRIES):
            try:
                return await self._perform_request(session, url, params)
            except ApiError as e:
                last_error = e
                if not e.retryable:
                    raise
                await self._handle_retry_error(e, attempt)

        logger.error(f"API полностью недоступно: {last_error}")
        raise last_error

    @staticmethod
    async def _handle_retry_error(
            error: ApiError,
            attempt: int
    ) -> None:
        logger.warning(
            f"Попытка {attempt + 1} из {app_config.MAX_RETRIES} "
            f"(status={error.status}): {error}"
        )

        if attempt < app_config.MAX_RETRIES - 1:
            delay = min(2 ** attempt, 10) + random.random()
            await asyncio.sleep(delay)

    async def fetch_currency_rates(self, session: aiohttp.ClientSession) -> Dict[str, float]:
        """Получает курсы фиатных валют (EUR, GBP, etc)."""
        params = {
            app_config.CURRENCY_PARAM_FROM: app_config.BASE_CURRENCY,
            app_config.CURRENCY_PARAM_TO: ",".join(app_config.SUPPORTED_CURRENCIES)
        }

        data = await self.fetch_json(session, app_config.CURRENCY_API_URL, params=params)
        rates = data.get('rates', {})

        self.validators.check_empty_currency(rates)
        return rates

    async def fetch_crypto_rates(self, session: aiohttp.ClientSession) -> Dict[str, float | None]:
        """Получает курсы криптовалют и приводит их к удобному формату."""
        params = {
            app_config.CRYPTO_PARAM_IDS: app_config.CRYPTO_IDS,
            app_config.CRYPTO_PARAM_VS: app_config.CRYPTO_VS_CURRENCY
        }

        data = await self.fetch_json(session, app_config.CRYPTO_API_URL, params=params)
        return {
            short_name: data.get(api_id, {}).get(app_config.CRYPTO_VS_CURRENCY)
            for short_name, api_id in app_config.CRYPTO_MAPPING.items()
        }

    async def fetch_all(self) -> RatesReport:
        """
        Основной метод входа.
        Создает единую сессию aiohttp и запускает параллельный сбор всех данных.
        """
        async with aiohttp.ClientSession() as session:
            currency, crypto = await asyncio.gather(
                self.fetch_currency_rates(session),
                self.fetch_crypto_rates(session),
            )

            return RatesReport(currency, crypto)
