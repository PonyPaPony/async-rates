import json
import os
import shutil
from AsyncRates import app_config
from AsyncRates.utils.logger import AppLogger
from datetime import datetime, timedelta

logger = AppLogger.get_logger(__name__)


class CacheManager:
    """
    Управляет локальным файловым кэшем в формате JSON.
    Реализует атомарную запись (защиту от повреждения файла) и кэширование в памяти (RAM).
    """

    def __init__(self, path=None):
        self.path = path or app_config.PATH_TO_CACHE
        self._memory_cache = None
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with open(self.path, 'w', encoding=app_config.ENCODING) as f:
                json.dump({}, f)
                logger.info(f"Cache file created at {self.path}")

    def load_cache(self) -> dict:
        """
        Загружает данные из кэша.
        Сначала пытается отдать данные из RAM, иначе читает диск.
        """
        if self._memory_cache is not None:
            return self._memory_cache

        try:
            data = self._read_file_from_disk()

            if data is None:
                data = {}

            self._memory_cache = data
            return data

        except json.JSONDecodeError:
            logger.error(f"Ошибка чтения JSON в '{self.path}'. Создаю бэкап.")
            self._handle_corrupted_file()
            return {}

        except OSError as e:
            logger.error(f"Ошибка доступа к файлу кэша '{self.path}': {e}")
            return {}

    def _handle_corrupted_file(self):
        if self.path.exists():
            self._create_backup()
        self._memory_cache = {}
        try:
            self.save_cache(app_config.EMPTY_CACHE)
        except Exception:
            logger.critical("Не удалось восстановить кэш")

    def _read_file_from_disk(self) -> dict | None:
        with open(self.path, encoding=app_config.ENCODING) as f:
            data = json.load(f)

            if not isinstance(data, dict):
                logger.warning(f"Кэш '{self.path}' поврежден (не dict), сбрасываю.")
                return None

        return data

    def _create_backup(self):
        """
        Создает резервную копию текущего файла кэша.

        Копирует поврежденный файл в новый файл с добавлением временной метки
        к имени (например, rates.json.bak_20231010_120000).
        Ошибки копирования логируются, но не прерывают выполнение программы.
        """
        try:
            timestamp = datetime.now().strftime(app_config.DATE_FORMAT_FOR_FILE)
            backup_path = f"{self.path}.bak_{timestamp}"
            shutil.copyfile(self.path, backup_path)
            logger.info(f"Backup created: {backup_path}")
        except OSError:
            logger.error(f"Не удалось создать бэкап для '{self.path}'")

    def save_cache(self, data: dict) -> None:
        temp_file = self.path.with_suffix(self.path.suffix + ".temp")
        wrapped = {
            app_config.CACHE_KEY_TIMESTAMP: datetime.now().strftime(app_config.DATE_FORMAT),
            app_config.CACHE_KEY_DATA: data
        }

        self._memory_cache = wrapped

        with open(temp_file, 'w', encoding=app_config.ENCODING) as f:
            json.dump(wrapped, f, ensure_ascii=False, indent=2)

        os.replace(temp_file, self.path)

    def is_cache_old(self, max_age_minutes=app_config.MAX_AGE_MINUTES) -> bool:
        cache = self.load_cache()
        if not cache or app_config.CACHE_KEY_TIMESTAMP not in cache:
            return True

        try:
            ts = datetime.strptime(cache[app_config.CACHE_KEY_TIMESTAMP], app_config.DATE_FORMAT)
            return (datetime.now() - ts) > timedelta(minutes=max_age_minutes)
        except ValueError:
            return True

    def get_data(self) -> dict | None:
        cache = self.load_cache()
        if cache and app_config.CACHE_KEY_DATA in cache:
            return cache[app_config.CACHE_KEY_DATA]
        return None

    def clear_cache(self):
        self.save_cache(app_config.EMPTY_CACHE)
        logger.info(f"Cache cleared: {self.path}")