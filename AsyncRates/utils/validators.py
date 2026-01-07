from typing import Mapping
from AsyncRates.utils.logger import AppLogger
from AsyncRates.utils.app_exceptions import ARateError


logger = AppLogger.get_logger(__name__)

class Validators:
    @staticmethod
    def check_empty_currency(data: Mapping) -> None:
        msg = "Currency API returned empty rates"
        if not data:
            logger.warning(msg, extra={"source": 'currency_api'})
            raise ARateError(msg)