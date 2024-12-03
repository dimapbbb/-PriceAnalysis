import unittest
from unittest import TestCase

from src.algorithm import Algorithm


class AlgorithmTestCase(TestCase):
    algorithm = Algorithm()

    # test params
    algorithm.base_all_volume = 1000
    algorithm.base_klines_count = 5
    algorithm.quote_all_volume = 500
    algorithm.quote_klines_count = 5
    algorithm.base_avg_volume = 200.0
    algorithm.quote_avg_volume = 100.0

    def test_compare_klines(self):
        """ Тестирование сравнения клайнов """
        base_kline = {
            'open': 100000,
            'close': 110000,    # change 10%
            'volume': 200       # not base_above_avg
        }
        quote_kline = {
            'open': 50000,
            'close': 55000,     # change 10%
            'volume': 100       # not quote_above_avg
        }
        self.assertEqual(self.algorithm.compare_klines(base_kline, quote_kline), 0.0)

        base_kline = {
            'open': 110000,
            'close': 100000,    # change -10%
            'volume': 200       # not base_above_avg
        }
        quote_kline = {
            'open': 55000,
            'close': 52500,     # change 10%
            'volume': 800       # quote_above_avg
        }
        self.assertEqual(self.algorithm.compare_klines(base_kline, quote_kline), -4.55)

        base_kline = {
            'open': 100000,
            'close': 120000,    # change 20%
            'volume': 1000      # base_above_avg
        }
        quote_kline = {
            'open': 50000,
            'close': 60000,     # change 20%
            'volume': 90        # not quote_above_avg
        }
        self.assertEqual(self.algorithm.compare_klines(base_kline, quote_kline), 20.0)

        base_kline = {
            'open': 100000,
            'close': 120000,    # change 20%
            'volume': 1000      # base_above_avg
        }
        quote_kline = {
            'open': 50000,
            'close': 55000,     # change 10%
            'volume': 200       # quote_above_avg
        }
        self.assertEqual(self.algorithm.compare_klines(base_kline, quote_kline), -10.0)

    def test_compare_current_volume(self):
        self.assertTrue(self.algorithm.compare_current_volume(200, 100))
        self.assertFalse(self.algorithm.compare_current_volume(100, 200))

    def test_calculate_price_change(self):
        """ Тест высчитывания процента изменения цены """
        # Повышение цены
        kline = {
            'open': 100,
            'close': 105
        }
        self.assertEqual(self.algorithm.calculate_price_change(kline), 5.0)
        # Понижение цены
        kline = {
            'open': 105,
            'close': 100
        }
        self.assertEqual(self.algorithm.calculate_price_change(kline), -4.76)
