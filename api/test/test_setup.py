from rest_framework.test import APITestCase


class TestSetUp(APITestCase):

    def setUp(self):
        self.valid_market_id = "BTC-CLP"
        self.valid_base_currency = "BTC"
        self.valid_quote_currency = "CLP"
        self.invalid_market_id = "loren_ipsum"
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
