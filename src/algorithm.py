class Algorithm:
    base_all_volume = quote_all_volume = 0       # Начальные значения общего объема торгов
    base_klines_count = quote_klines_count = 0   # Начальные значения количества полученных клайнов
    base_avg_volume = quote_avg_volume = 0       # Начальные значения среднего объема торгов

    def __init__(self, custom_excess=0):
        self.custom_excess = custom_excess

    def compare_klines(self, base:dict, quote:dict):
        """
        Сравнение клайнов входящих цен
        :param base: Актив, влияние которого нужно убрать
        :param quote: Актив, собственное изменение которого нужно вычислить
        :return: Собственное изменение цены котируемого актива в процентах
        """
        self.calculate_avg_volumes(base['volume'], quote['volume'])

        base_above_avg = self.compare_current_volume(base['volume'], self.base_avg_volume)
        quote_above_avg = self.compare_current_volume(quote['volume'], self.quote_avg_volume)

        base_price_change = self.calculate_price_change(base)
        quote_price_change = self.calculate_price_change(quote)

        if (base_above_avg and quote_above_avg) or (not base_above_avg and not quote_above_avg):
            return round(quote_price_change - base_price_change, 2)
        else:
            return round(quote_price_change, 2)

    def compare_current_volume(self, volume:float, avg:float):
        """
        Сравнивает текущий объем со средним значением, умноженным на пользовательский коэффициент
        :param volume: Объем торгов за последний клайн
        :param avg: Средний объем торгов с момента начала работы
        :return: Булево значение
        """
        return volume > avg * (1 + self.custom_excess / 100)

    def calculate_avg_volumes(self, base:float, quote:float):
        """
        Вычисление среднего объема торгов начиная с момента начала работы
        """
        self.base_all_volume += base
        self.quote_all_volume += quote
        self.base_klines_count += 1
        self.quote_klines_count += 1

        self.base_avg_volume = round(self.base_all_volume / self.base_klines_count, 5)
        self.quote_avg_volume = round(self.quote_all_volume / self.quote_klines_count, 5)

    @staticmethod
    def calculate_price_change(kline:dict):
        """
        Вычисление процентного изменения цены клайна
        :return: процент на который изменилась цена в течении клайна (отрицательное значение при падении цены)
        """
        price_change = (kline['close'] - kline['open']) / kline['open'] * 100
        return price_change