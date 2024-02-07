from .test_setup import TestSetUp
from ..models import Market, Ticker, Spread
from decimal import Decimal


class TestModels(TestSetUp):
    """
    Tests for `Market`, `Ticker` and `Spreads` models.
    """

    def test_create_valid_market(self):
        """
        Valid `Market` object creation
        """
        market = Market(self.valid_market_id)
        self.assertEqual(market.id, self.valid_market_id)
        self.assertEqual(market.base_currency, self.valid_base_currency)
        self.assertEqual(market.quote_currency, self.valid_quote_currency)
        self.assertTrue(isinstance(market.min_order_amount_value, Decimal))

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
