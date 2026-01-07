import asyncio

from AsyncRates.utils.logger import AppLogger
from AsyncRates.services.api_client import ApiClient
from AsyncRates.services.cache_manager import CacheManager
from AsyncRates.services.rate_manager import RateManager
from AsyncRates.utils.app_exceptions import ARateError

async def main():
    logger = AppLogger.get_logger(__name__)

    client = ApiClient()
    cache = CacheManager()

    manager = RateManager(api_client=client, cache_manager=cache)

    try:
        result = await manager.get_rates()
        logger.info("\n--- РЕЗУЛЬТАТ ---\n%s", result)
    except ARateError as e:
        logger.error("Ошибка API: %s", e)
    except Exception:
        logger.exception("Неожиданная ошибка")

if __name__ == '__main__':
    AppLogger.setup()
    asyncio.run(main())
