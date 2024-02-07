from django.db import models
from .buda_utils import fetch_data
from decimal import Decimal


class Market(models.Model):
    """
    `Market` object that stores all data returned from `/markets/{market_id}`

    To initialize you must provide one of these arguments: a `market_id` to
    retrieve the data directly from Buda.com API, or a dictionary already
    populated with the required data. If you provide both, the dictionary
    takes precedence.

    :param market_id: valid market identifier, e.g. `btc-clp`
    :param market: dictionary with all required data to initialize the object
    """

    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    base_currency = models.CharField(max_length=15)
    quote_currency = models.CharField(max_length=15)
    max_orders_per_minute = models.PositiveSmallIntegerField()

    # Minumum order amount accepted.
    min_order_amount_value = models.DecimalField(
        max_digits=22, decimal_places=10
    )  # noqa: E501
    min_order_amount_currency = models.CharField(max_length=15)

    # Fees and discounts for takers and makers orders
    taker_fee = models.DecimalField(max_digits=22, decimal_places=10)
    taker_discount_percentage = models.DecimalField(
        max_digits=22, decimal_places=10
    )  # noqa: E501
    maker_fee = models.DecimalField(max_digits=22, decimal_places=10)
    maker_discount_percentage = models.DecimalField(
        max_digits=22, decimal_places=10
    )  # noqa: E501

    def __init__(self, market_id: str = "", market: dict = {}):

        if not market:
            # retrieve data for the given market
            # and asign it to the market dict
            endpoint = f"/markets/{market_id}"
            market = fetch_data(endpoint)["market"]

        # assign to its corresponding attributes
        self.id = market["id"]
        self.name = market["name"]
        self.base_currency = market["base_currency"]
        self.quote_currency = market["quote_currency"]
        self.max_orders_per_minute = int(market["max_orders_per_minute"])

        # The API return this as an array, where the first element
        # is the amount and the second is the currency code.
        # We save each value separately for easy managment.
        self.min_order_amount_value = Decimal(
            market["minimum_order_amount"][0]
        )  # noqa: E501
        self.min_order_amount_currency = market["minimum_order_amount"][1]

        self.taker_fee = Decimal(market["taker_fee"])
        self.taker_discount_percentage = Decimal(
            market["taker_discount_percentage"]
        )  # noqa: E501
        self.maker_fee = Decimal(market["maker_fee"])
        self.maker_discount_percentage = Decimal(
            market["maker_discount_percentage"]
        )  # noqa: E501

    @classmethod
    def get_all_markets(cls):
        """
        Retrieves a list with all markets from Buda.com API

        :return: A list of `Market` objects
        """
        endpoint = "/markets"
        markets = []
        markets_data = fetch_data(endpoint)["markets"]

        for market_data in markets_data:
            markets.append(cls("", market_data))

        return markets

    class Meta:
        managed = False


class Ticker(models.Model):
    """
    `Ticker` object that stores all data returned from
    `/markets/{market_id}/ticker` endpoint.

    To initialize:
    :param market_id: valid market identifier, e.g. `btc-clp`
    """

    market_id = models.CharField(max_length=30)

    price_variation_24h = models.DecimalField(max_digits=10, decimal_places=5)
    price_variation_7d = models.DecimalField(max_digits=10, decimal_places=5)

    # latest executed order price
    last_price_value = models.DecimalField(max_digits=22, decimal_places=10)
    last_price_currency = models.CharField(max_length=15)

    # higher bid price
    max_bid_value = models.DecimalField(max_digits=22, decimal_places=10)
    max_bid_currency = models.CharField(max_length=15)

    # lower ask price
    min_ask_value = models.DecimalField(max_digits=22, decimal_places=10)
    min_ask_currency = models.CharField(max_length=15)

    # volume traded during the latest 24 hours
    volume_value = models.DecimalField(max_digits=22, decimal_places=10)
    volume_currency = models.CharField(max_length=15)

    fetch_date = models.DateTimeField(auto_now_add=True)

    def __init__(self, market_id: str):
        # retrieve the ticket for the specific market
        endpoint = f"/markets/{market_id}/ticker"
        ticker = fetch_data(endpoint)["ticker"]  # TODO: ?

        # assign the values to its corresponding attributes...

        self.market_id = ticker["market_id"]
        self.price_variation_24h = Decimal(ticker["price_variation_24h"])
        self.price_variation_7d = Decimal(ticker["price_variation_7d"])

        # The API return all figures as an array, where the first
        # element is the amount and the second is the currency code.
        # We save each value separately for easy managment.
        self.last_price_value = Decimal(ticker["last_price"][0])
        self.last_price_currency = ticker["last_price"][1]
        self.max_bid_value = Decimal(ticker["max_bid"][0])
        self.max_bid_currency = ticker["max_bid"][1]
        self.min_ask_value = Decimal(ticker["min_ask"][0])
        self.min_ask_currency = ticker["min_ask"][1]
        self.volume_value = Decimal(ticker["volume"][0])
        self.volume_currency = ticker["volume"][1]

    class Meta:
        managed = False


class Spread(models.Model):
    """
    `Spread` object that calculates the current spread of a given market.

    To initialize:
    :param market_id: valid market identifier, e.g. `btc-clp`
    """

    market_id = models.CharField(max_length=30)
    value = models.DecimalField(max_digits=22, decimal_places=10)
    currency = models.CharField(max_length=15)
    fetch_date = models.DateTimeField(auto_now_add=True)

    def __init__(self, market_id: str):
        # get the ticker for the given market
        ticker = Ticker(market_id)

        # assign the values to its corresponding attributes...
        self.market_id = ticker.market_id
        self.value = ticker.min_ask_value - ticker.max_bid_value
        self.currency = ticker.max_bid_currency

    @classmethod
    def get_all_markets_spread(cls) -> list:
        pass
