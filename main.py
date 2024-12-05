from threading import Timer
from datetime import datetime
from time import sleep

from config import BASE_COIN, QUOTE_COIN, INTERVAL, KLINE_QTY
from src.algorithm import Algorithm
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
            interval='D' if interval == 1440 else str(interval)
        )
        self.quote_coin = ByBit(
            symbol=self.quote_coin,
            interval='D' if interval == 1440 else str(interval)
        )

    def start_work(self):
        """ Задержка перед началом работы позволяющая получать клайны через 3 секунды после их завершения """
        while True:
            now = datetime.now()
            if (int(now.hour) * 60 * 60 + int(now.minute) * 60 + int(now.second)) % self.interval == 0:
                sleep(2)
                return self.work()
            sleep(1)

    def work(self):
        """ Рекурсивный вызов итерации в одно и то же время согласно интервалу """
        Timer(self.interval, self.work).start()
        self.iterate()

    def iterate(self):
        """ Одна, совершаемая ботом итерация """
        base_kline = self.base_coin.get_kline()[0]
        quote_kline = self.quote_coin.get_kline()[0]

        self.algorithm.print_own_price_change(modified_(base_kline), modified_(quote_kline))

    def history_analysis(self, kline_qty:int=1000):
        """ Исследование <kline_qty> последних клайнов """
        kline_qty = 1000 if kline_qty > 1000 else kline_qty

        base_history = self.base_coin.get_kline(kline_qty=kline_qty)
        quote_history = self.quote_coin.get_kline(kline_qty=kline_qty)

        for base_kline, quote_kline in zip(base_history[::-1], quote_history[::-1]):
            self.algorithm.print_own_price_change(modified_(base_kline), modified_(quote_kline))


if __name__ == '__main__':
    bot = Bot(
        base_coin=BASE_COIN,
        quote_coin=QUOTE_COIN,
        interval=INTERVAL,
    )
    bot.history_analysis(kline_qty=KLINE_QTY)
    bot.start_work()
