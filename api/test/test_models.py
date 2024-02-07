from .test_setup import TestSetUp
from ..models import Ticker, Spread
from decimal import Decimal


class TestModels(TestSetUp):
    """
    Tests for `Ticker` and `Spreads` models.
    """

    def test_create_valid_ticker(self):
        """
        Valid `Ticker` object creation
        """
        ticker = Ticker(self.valid_market_id)
        self.assertEqual(ticker.volume_currency, self.valid_base_currency)
        self.assertEqual(ticker.last_price_currency, self.valid_quote_currency)

    def test_create_valid_spread(self):
        """
        Valid `Spread` object creation
        """
        spread = Spread(self.valid_market_id)
        self.assertEqual(spread.market_id, self.valid_market_id)
        self.assertTrue(isinstance(spread.value, Decimal))
