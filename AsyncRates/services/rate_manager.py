from AsyncRates import app_config
from AsyncRates.app_models.reports import RatesReport
from AsyncRates.utils.logger import AppLogger
from AsyncRates.utils.app_exceptions import ARateError

logger = AppLogger.get_logger(__name__)


class RateManager:
    """
    Фасад, управляющий получением данных.
    Решает, откуда брать данные: из кэша или из API.
    Реализует стратегию Fallback (откат к старым данным при сбое API).
    """
    def __init__(self, api_client, cache_manager):
        self.api_client = api_client
        self.cache_manager = cache_manager

    async def get_rates(self) -> RatesReport:
        """
        Главный метод получения курсов.
        Алгоритм:
        1. Если кэш есть и он свежий -> возвращаем кэш.
        2. Если кэш старый или его нет -> пытаемся получить из API.
        3. Если API ответил -> обновляем кэш и возвращаем.
        4. Если API упал -> пробуем вернуть ХОТЯ БЫ старый кэш (с warning).
        5. Если и кэша нет, и API упал -> пробрасываем ошибку.
        """
        if not self.cache_manager.is_cache_old():
            logger.info("Кэш актуален. Возвращаю данные из памяти/файла.")
            return self._load_from_cache()

        logger.info("Кэш устарел или отсутствует. Пробую обновить через API...")

        try:
            return await self._get_report()
        except ARateError as e:
            return self._fallback(e)

    async def _get_report(self) -> RatesReport:
        report = await self.api_client.fetch_all()

        data_to_save = {
            app_config.CUR_KEY: report.currency,
            app_config.CRY_KEY: report.crypto,
        }

        self.cache_manager.save_cache(data_to_save)
        logger.info("Данные успешно обновлены из API.")
        return report

    def _fallback(self, error: Exception) -> RatesReport:
        logger.warning(f"Не удалось обновить данные через API: {error}")

        cached_data = self.cache_manager.get_data()
        if cached_data:
            logger.warning("!!! ВНИМАНИЕ: Возвращаю устаревшие данные из кэша !!!")
            return self._load_from_cache()

        logger.error("Нет ни свежих данных, ни кэша. Работа невозможна.")
        raise ARateError("Rates unavailable")

    def _load_from_cache(self):
        """Вспомогательный метод для превращения dict из кэша в объект RatesReport."""
        data = self.cache_manager.get_data()

        if not data:
            raise ValueError("Кэш пуст и не может быть использован для fallback")

        return RatesReport(
            currency=data.get(app_config.CUR_KEY, {}),
            crypto=data.get(app_config.CRY_KEY, {})
        )