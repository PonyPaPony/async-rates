import sys
import logging
from logging.handlers import RotatingFileHandler
from AsyncRates import app_config


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "source"):
            record.source = "app"
        return True


class AppLogger:
    """
    Класс для логирования приложения
    """

    _is_setup = False
    LOGGER_NAME = app_config.LOGGER_NAME


    @staticmethod
    def setup():
        if AppLogger._is_setup:
            return

        AppLogger.ensure_log_folder()
        context_filter = ContextFilter()

        logger = logging.getLogger(AppLogger.LOGGER_NAME)

        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        formatter = logging.Formatter(app_config.LOG_FORMAT)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(context_filter)

        file_handler = RotatingFileHandler(
            app_config.LOG_PATH,
            maxBytes=app_config.LOG_MAX_BYTES,
            backupCount=app_config.LOG_BACKUP_COUNT,
            encoding=app_config.ENCODING,
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(context_filter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        AppLogger._is_setup = True

    @staticmethod
    def ensure_log_folder():
        app_config.LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Возвращает дочерний логгер приложения
        """
        if not AppLogger._is_setup:
            AppLogger.setup()

        return logging.getLogger(f"{AppLogger.LOGGER_NAME}.{name}")