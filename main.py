from src.algorithm import Algorithm
from src.config import BASE_COIN, QUOTE_COIN, INTERVAL
from src.foonctools import modified_
from src.provider import ByBit


class Bot:
    def __init__(self, base_coin='BTC', quote_coin='ETH', interval='60'):
        self.base_coin = base_coin.upper() + 'USDT'
        self.quote_coin = quote_coin.upper() + 'USDT'
        self.interval = interval
        self.algorithm = Algorithm()
        self.base_coin = ByBit(
            symbol=self.base_coin,
            interval=self.interval
        )
        self.quote_coin = ByBit(
            symbol=self.quote_coin,
            interval=self.interval
        )

    def work(self):
        while True:
            self.trigger_for_get_kline()

            base_kline = modified_(self.base_coin.get_kline())
            quote_kline = modified_(self.quote_coin.get_kline())

            own_price_change = self.algorithm.compare_klines(base_kline, quote_kline)
            if own_price_change >= 1:
                print(f"Цена выросла на {own_price_change}%")
            elif own_price_change <= -1:
                print(f"Цена упала на {own_price_change}%")

    def trigger_for_get_kline(self):
        pass

if __name__ == '__main__':
    Bot(
        base_coin=BASE_COIN,
        quote_coin=QUOTE_COIN,
        interval=INTERVAL,
    ).work()