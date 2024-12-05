import unittest
from unittest import TestCase

from main import Bot


class BotTestCase(TestCase):
    test_bot = Bot()

    def test_trigger_first_iteration(self):
        pass