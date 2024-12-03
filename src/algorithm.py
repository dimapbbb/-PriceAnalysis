from src.config import BASE_CUSTOM_EXCESS, QUOTE_CUSTOM_EXCESS


class Algorithm:
    base_all_volume = quote_all_volume = 0         # Начальные значения общего объема торгов базового актива
    base_klines_count = quote_klines_count = 0     # Начальные значения общего объема торгов котируемого актива


    def compare_klines(self, base:dict, quote:dict):
        """
        Сравнение клайнов входящих цен
        :param base: Актив, влияние которого нужно убрать
        :param quote: Актив, собственное изменение которого нужно вычислить
        :return: Собственное изменение цены котируемого актива в процентах
        """
        base_avg_volume, quote_avg_volume = self.calculate_avg_volume(base['volume'], quote['volume'])

        base_price_change = self.calculate_price_change(base)
        quote_price_change = self.calculate_price_change(quote)

        if base['volume'] > base_avg_volume * (1 + BASE_CUSTOM_EXCESS / 100):
            if quote['volume'] > quote_avg_volume * (1 + QUOTE_CUSTOM_EXCESS / 100):
                own_price_change = quote_price_change - base_price_change
            else:
                own_price_change = quote_price_change

        else:
            if quote['volume'] > quote_avg_volume * (1 + QUOTE_CUSTOM_EXCESS / 100):
                own_price_change = quote_price_change
            else:
                own_price_change = quote_price_change - base_price_change

        return own_price_change


    def calculate_avg_volume(self, base:float, quote:float):
        """
        Вычисление среднего объема торгов начиная с момента начала работы
        :return: Средний объем торгов за клайн
        """
        self.base_all_volume += base
        self.quote_all_volume += quote
        self.base_klines_count += 1
        self.quote_klines_count += 1

        base_avg = self.base_all_volume / self.quote_all_volume
        quote_avg = self.quote_all_volume / self.quote_klines_count

        return round(base_avg, 5), round(quote_avg, 5)

    @staticmethod
    def calculate_price_change(kline:dict):
        """
        Вычисление процентного изменения цены клайна
        :return: процент на который изменилась цена в течении клайна (отрицательное значение при падении цены)
        """
        price_change = (kline['close'] - kline['open']) / kline['open'] * 100
        return round(price_change, 2)