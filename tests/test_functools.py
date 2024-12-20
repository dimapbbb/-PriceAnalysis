from unittest import TestCase

from src.functools import modified_


class FunctoolsTestCase(TestCase):

    def test_modified_(self):
        test_kline = ['12344550000', '300.45', 'some_value', 'some_value', '555.45', '1234.56', 'some_value']
        result_kline = {
            'timestamp': 12344550000,
            'open': 300.45,
            'close': 555.45,
            'volume': 1234.56
        }
        self.assertEqual(modified_(test_kline), result_kline)
