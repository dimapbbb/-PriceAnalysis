from threading import Timer
from datetime import datetime
from time import sleep

from src.algorithm import Algorithm
from config import BASE_COIN, QUOTE_COIN, INTERVAL
from src.functools import modified_
from src.provider import ByBit


class Bot:
    def __init__(self, base_coin='BTC', quote_coin='ETH', interval=60):
        self.base_coin = base_coin.upper() + 'USDT'
        self.quote_coin = quote_coin.upper() + 'USDT'
        self.interval = interval * 60
        self.algorithm = Algorithm()
        self.base_coin = ByBit(
            symbol=self.base_coin,
            interval=str(self.interval)
        )
        self.quote_coin = ByBit(
            symbol=self.quote_coin,
            interval=str(self.interval)
        )

    def work(self):
        """ Продолжение работы в реальном времени """
        self.restarter(self.interval, self.iterate)

    def restarter(self, interval, func):
        """
        Перезапуск каждой итерации через интервал
        :param interval: Время в секундах
        :param func: Функция, которую надо перезапускать
        """
        Timer(interval, self.restarter, [interval, func]).start()
        func()

    def iterate(self):
        """ Одна, совершаемая ботом итерация """
        base_kline = self.base_coin.get_kline()[-1]
        quote_kline = self.quote_coin.get_kline()[-1]

        if base_kline and quote_kline:
            own_price_change = self.algorithm.compare_klines(modified_(base_kline), modified_(quote_kline))
            print(f"{own_price_change}%", datetime.now())
        else:
            print('Данные не предоставлены')

    def start_work(self):
        """ Задержка перед началом работы позволяющая получать клайны через 3 секунды после их завершения """
        while True:
            now = datetime.now()
            if (int(now.hour) * 60 * 60 + int(now.minute) * 60 + int(now.second)) % self.interval == 0:
                sleep(2)
                return self.work()
            sleep(1)


if __name__ == '__main__':
    Bot(
        base_coin=BASE_COIN,
        quote_coin=QUOTE_COIN,
        interval=INTERVAL,
    ).start_work()
