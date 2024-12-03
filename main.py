from threading import Timer
from datetime import datetime
from time import sleep

from src.algorithm import Algorithm
from src.config import BASE_COIN, QUOTE_COIN, INTERVAL
from src.functools import modified_
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
        """ Бесконечный цикл для продолжения работы в реальном времени """
        interval = int(self.interval)
        self.trigger_first_iteration(interval)
        self.restarter(interval*60, self.iterate)

    def restarter(self, interval, func):
        """
        Постоянный перезапуск функции через интервал
        :param interval: Время в секундах
        :param func: Функция, которую надо перезапускать
        """
        Timer(interval, self.restarter, [interval, func]).start()
        func()

    def iterate(self):
        """ Одна совершаемая ботом итерация """
        base_kline = self.base_coin.get_kline()[-1]
        quote_kline = self.quote_coin.get_kline()[-1]

        own_price_change = self.algorithm.compare_klines(modified_(base_kline), modified_(quote_kline))
        print(f"{own_price_change}%")

    @staticmethod
    def trigger_first_iteration(interval):
        """ Запуск первой итерации по времени в зависимости от интервала """
        if interval < 60:
            while True:
                if int(str(datetime.now())[14:16]) % interval == 0 and str(datetime.now())[17:19] == '00':
                    sleep(2)
                    return
                sleep(1)

        elif interval <= 1440:
            while True:
                if int(str(datetime.now())[11:13]) % interval / 60 == 0 and str(datetime.now())[14:16] == '00':
                    sleep(2)
                    return
                sleep(60)


if __name__ == '__main__':
    Bot(
        base_coin=BASE_COIN,
        quote_coin=QUOTE_COIN,
        interval=INTERVAL,
    ).work()