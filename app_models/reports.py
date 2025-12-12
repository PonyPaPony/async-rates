class RatesReport:
    """
    Представляет отчет о курсах валют и криптовалют.

    Этот класс генерирует форматированное представление курсов обмена как для
    обычных валют, так и для криптовалют.

    :ivar currency: Словарь, сопоставляющий коды валют с их курсами
        относительно USD.
    :type currency: Dict
    :ivar crypto: Словарь, сопоставляющий названия криптовалют с их ценами в USD.
    :type crypto: Dict
    """
    def __init__(self, currency: dict, crypto: dict):
        self.currency = currency
        self.crypto = crypto

    def __str__(self):
        lines = ["====== КУРСЫ ВАЛЮТ ======"]
        for cur, rate in self.currency.items():
            lines.append(f"💵 USD -> {cur}: {rate:.4f}")

        lines.append("\n====== КРИПТОВАЛЮТА ======")
        for coin, price in self.crypto.items():
            lines.append(f"🪙 {coin}: ${price:,.2f}")

        return "\n".join(lines)