from .test_setup import TestSetUp
from ..models import Market, Ticker, Spread, Polling
from decimal import Decimal
from random import choice


class TestModels(TestSetUp):
    """
    Tests for `Market`, `Ticker` and `Spreads` models.
    """

    def test_create_valid_market(self):
        """
        Valid `Market` object creation
        """
        market = Market.create(self.valid_market_id)
        self.assertEqual(market.id, self.valid_market_id)
        self.assertEqual(market.base_currency, self.valid_base_currency)
        self.assertEqual(market.quote_currency, self.valid_quote_currency)
        self.assertTrue(isinstance(market.min_order_amount_value, Decimal))

    def test_retrieve_all_markets(self):
        """
        Valid markets retrieving
        """
        markets = Market.get_all_markets()
        self.assertTrue(isinstance(markets, list))
        self.assertTrue(isinstance(choice(markets), Market))

    def test_create_valid_ticker(self):
        """
        Valid `Ticker` object creation
        """
        ticker = Ticker.create(self.valid_market_id)
        self.assertEqual(ticker.volume_currency, self.valid_base_currency)
        self.assertEqual(ticker.last_price_currency, self.valid_quote_currency)

    def test_create_valid_spread(self):
        """
        Valid `Spread` object creation
        """
        spread = Spread.create(self.valid_market_id)
        self.assertEqual(spread.market_id, self.valid_market_id)
        self.assertTrue(isinstance(spread.value, Decimal))

    def test_get_each_markets_spread(self):
        spreads = Spread.get_each_markets_spread()
        self.assertTrue(isinstance(spreads, list))
        self.assertTrue(isinstance(choice(spreads), Spread))

    def test_create_valid_polling(self):
        spread = Spread.create(self.valid_market_id)
        polling = Polling.create(spread)

        self.assertTrue(isinstance(polling, Polling))
        self.assertEqual(polling.market_id, self.valid_market_id)
        self.assertTrue(
            polling.difference == 0
            or polling.current_is_greater
            or polling.stored_is_greater
        )
