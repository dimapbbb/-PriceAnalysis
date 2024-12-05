from pybit.unified_trading import HTTP


class ByBit:
    """
    Биржа поставляющая цены
    ПО умолчанию рынок бессрочных фьючерсов
    """
    def __init__(self, symbol, interval, category='linear'):
        self.symbol = symbol
        self.interval = interval
        self.category = category
        self.session = HTTP(testnet=False)

    def get_kline(self, kline_qty:int=1):
        """
        Получение данных о цене (последний завершенный клайн по умолчанию)
        :param kline_qty: количество последних клайнов (Не более 1000 - ограничение биржы)
        :return: список завершенных свечей (по устареванию)
        [["dt", "open", "high", "low", "close", "объем", "оборот"], [...], ... ]
        """

        response = self.session.get_kline(
            category=self.category,
            symbol=self.symbol,
            interval=self.interval,
            limit=kline_qty + 1
        )
        return response.get('result').get('list')[1:]



