from rest_framework.test import APITestCase


class TestSetUp(APITestCase):

    def setUp(self):
        # valid data set
        self.valid_market_id = "BTC-CLP"
        self.valid_base_currency = "BTC"
        self.valid_quote_currency = "CLP"
        self.valid_market_data = {
            "id": "USDC-CLP",
            "name": "usdc-clp",
            "base_currency": "USDC",
            "quote_currency": "CLP",
            "minimum_order_amount": ["0.00000001", "USDC"],
            "taker_fee": "0.8",
            "maker_fee": "0.4",
            "max_orders_per_minute": 150,
            "maker_discount_percentage": "0.1",
            "taker_discount_percentage": "0.2",
        }

        # invalid data set
        self.invalid_market_id = "loren_ipsum"
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
