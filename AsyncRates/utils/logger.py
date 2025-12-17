import os
import logging
from AsyncRates import app_config


class AppLogger:
    """Централизованная настройка логгирования."""

    _is_setup = False

    @staticmethod
    def setup():
        """
        Настраивает конфигурацию логгирования.
        Должен вызываться один раз при старте приложения.
        """
        if AppLogger._is_setup:
            return

        AppLogger.log_folder_check()

        logging.basicConfig(
            level=logging.INFO,
            format=app_config.LOG_FORMAT,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(app_config.LOG_PATH, encoding=app_config.ENCODING)
            ]
        )
        AppLogger._is_setup = True

    @staticmethod
    def log_folder_check():
        """Создает папку для логов, если её нет."""
        log_dir = os.path.dirname(app_config.LOG_PATH)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    @staticmethod
    def get_logger(name: str):
        """
        Возвращает именованный логгер.
        Пример: logger = AppLogger.get_logger(__name__)
        """
        if not AppLogger._is_setup:
            AppLogger.setup()

        return logging.getLogger(name)
