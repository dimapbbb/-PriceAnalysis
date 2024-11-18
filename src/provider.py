from pybit.unified_trading import HTTP


class ByBit:
    """
    Биржа поставляющая цены
    """
    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.category = "spot"
        self.session = HTTP(testnet=False)

    def get_kline(self):
        """ Получение последнего завершенного клайна """
        response = self.session.get_kline(
            category=self.category,
            symbol=self.symbol,
            interval=self.interval
        )
        return response.get('result').get('list')[1]



