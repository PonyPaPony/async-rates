import json
import os
import shutil
import app_config
from utils import AppLogger
from datetime import datetime, timedelta

logger = AppLogger.get_logger(__name__)


class CacheManager:
    """
    Управляет локальным файловым кэшем в формате JSON.
    Реализует атомарную запись (защиту от повреждения файла) и кэширование в памяти (RAM).
    """

    def __init__(self, path=app_config.PATH_TO_CACHE):
        """
        Инициализирует менеджер кэша.

        :param path: Путь к JSON-файлу кэша.
        """
        self.path = path
        self._memory_cache = None
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """
        Внутренний метод. Создает директорию и пустой JSON-файл,
        если они не существуют.
        """
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding=app_config.ENCODING) as f:
                json.dump({}, f)

    def load_cache(self) -> dict | None:
        """
        Загружает данные из кэша.
        Сначала пытается отдать данные из RAM, иначе читает диск.
        """
        # 1. Быстрый возврат из памяти
        if self._memory_cache is not None:
            return self._memory_cache

        # 2. Попытка чтения с диска
        try:
            data = self._read_file_from_disk()

            # Если вернулся None (не dict), считаем кэш пустым, чтобы не читать диск снова
            if data is None:
                self._memory_cache = {}

            # Если всё ок
            self._memory_cache = data
            return data

        except json.JSONDecodeError:
            # 3. Обработка битого JSON
            logger.error(f"Ошибка чтения JSON в '{self.path}'. Создаю бэкап.")
            self._handle_corrupted_file()
            return None

        except OSError as e:
            # 4. Обработка ошибок доступа
            logger.error(f"Ошибка доступа к файлу кэша '{self.path}': {e}")
            return None

    def _handle_corrupted_file(self):
        """Обрабатывает ситуацию с битым файлом: делает бэкап и сбрасывает кэш."""
        if os.path.exists(self.path):
            self._create_backup()
        self._memory_cache = {}

    def _read_file_from_disk(self) -> dict | None:
        """
        Внутренний метод: читает файл с диска и парсит JSON.

        :return: Словарь данных или None, если файл содержит не dict.
        :raises: json.JSONDecodeError, OSError (пробрасываются наверх)
        """
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
            logger.info(f"Бэкап сохранен: {backup_path}")
        except OSError:
            logger.error(f"Не удалось создать бэкап для '{self.path}'")

    def save_cache(self, data: dict) -> None:
        """
        Сохраняет данные в кэш.
        Использует технику атомарной записи (write to temp -> rename),
        чтобы избежать потери данных при сбое программы.
        """
        temp_file = self.path + ".tmp"
        wrapped = {
            app_config.CACHE_KEY_TIMESTAMP: datetime.now().strftime(app_config.DATE_FORMAT),
            app_config.CACHE_KEY_DATA: data
        }

        # Сразу обновляем память, чтобы не перечитывать диск
        self._memory_cache = wrapped

        with open(temp_file, 'w', encoding=app_config.ENCODING) as f:
            json.dump(wrapped, f, ensure_ascii=False, indent=2)

        os.replace(temp_file, self.path)

    def is_cache_old(self, max_age_minutes=app_config.MAX_AGE_MINUTES) -> bool:
        """
        Проверяет, устарел ли кэш.

        :param max_age_minutes: Время жизни кэша в минутах.
        :return: True, если кэш старый или отсутствует, иначе False.
        """
        cache = self.load_cache()
        if not cache or app_config.CACHE_KEY_TIMESTAMP not in cache:
            return True

        try:
            ts = datetime.strptime(cache[app_config.CACHE_KEY_TIMESTAMP], app_config.DATE_FORMAT)
            return (datetime.now() - ts) > timedelta(minutes=max_age_minutes)
        except ValueError:
            return True

    def get_data(self) -> dict | None:
        """
        Возвращает чистые данные (без метки времени).

        :return: Словарь с данными или None.
        """
        cache = self.load_cache()
        if cache and app_config.CACHE_KEY_DATA in cache:
            return cache[app_config.CACHE_KEY_DATA]
        return None

    def clear_cache(self):
        """Очищает кэш, перезаписывая его пустым словарем."""
        self.save_cache({})
        logger.info(f"Кэш очищен: {self.path}")