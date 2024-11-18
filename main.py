from src.config import BASE_COIN, QUOTE_COIN, INTERVAL
from src.provider import ByBit


class Bot:
    def __init__(self, base_coin='BTCUSDT', quote_coin='ETHUSDT', interval='60'):
        self.base_coin = base_coin
        self.quote_coin = quote_coin
        self.interval = interval

    def start_work(self):
        base_coin = ByBit(
            symbol=self.base_coin,
            interval=self.interval
        )
        quote_coin = ByBit(
            symbol=self.quote_coin,
            interval=self.interval
        )
        print(base_coin.get_kline())
        print(quote_coin.get_kline())


if __name__ == '__main__':
    Bot(
        base_coin=BASE_COIN,
        quote_coin=QUOTE_COIN,
        interval=INTERVAL,
    ).start_work()