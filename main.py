import asyncio
from utils import AppLogger
from services.api_client import ApiClient
from services.cache_manager import CacheManager
from services.rate_manager import RateManager

AppLogger.setup()


async def main():
    logger = AppLogger.get_logger(__name__)

    client = ApiClient()
    cache = CacheManager()

    manager = RateManager(api_client=client, cache_manager=cache)

    try:
        result = await manager.get_rates()
        logger.info("\n--- РЕЗУЛЬТАТ ---\n%s", result)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")


if __name__ == '__main__':
    asyncio.run(main())