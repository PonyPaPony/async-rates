import logging


class Validators:

    @staticmethod
    def check_empty_currency(data: dict):
        if not data:
            logging.warning("Currency API returned empty 'rates'")
            raise ValueError("Currency API returned empty data")