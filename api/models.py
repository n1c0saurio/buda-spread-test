from django.db import models
from buda.utils import fetch_data
from decimal import Decimal


class Market(models.Model):
    """
    A class that stores all data returned from `/markets/{market_id}`
    Buda.com API endpoint.

    To initialize you must provide one of these arguments: a `market_id` to
    retrieve the data directly from Buda.com API, or a dictionary already
    populated with the required data. If you provide both, the dictionary
    takes precedence.

    USAGE:
    >>> market = Market(market_id: str)
    >>> market = Market("", market_data: dict)
    """

    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    base_currency = models.CharField(max_length=15)
    quote_currency = models.CharField(max_length=15)
    max_orders_per_minute = models.PositiveSmallIntegerField()

    # Minumum order amount accepted.
    min_order_amount_currency = models.CharField(max_length=15)
    min_order_amount_value = models.DecimalField(
        max_digits=22,
        decimal_places=10,
    )

    # Fees and discounts for takers orders
    taker_fee = models.DecimalField(
        max_digits=22,
        decimal_places=10,
    )
    taker_discount_percentage = models.DecimalField(
        max_digits=22,
        decimal_places=10,
    )

    # Fees and discounts for makers orders
    maker_fee = models.DecimalField(
        max_digits=22,
        decimal_places=10,
    )
    maker_discount_percentage = models.DecimalField(
        max_digits=22,
        decimal_places=10,
    )

    @classmethod
    def create(cls, market_id: str = "", market_data: dict = {}):
        """
        Custom method to initialize a :class:`Market` instance.

        :param str market_id: valid market identifier, e.g. `btc-clp`.
        :param dict market_data: already populated with all required
        data to initialize the object.
        :rtype: Market
        """

        if not market_data:
            # retrieve data for the given market
            # and asign it to the dict
            endpoint = f"/markets/{market_id}"
            market_data = fetch_data(endpoint)["market"]

        # create the instance
        market = cls(
            id=market_data["id"],
            name=market_data["name"],
            base_currency=market_data["base_currency"],
            quote_currency=market_data["quote_currency"],
            max_orders_per_minute=int(market_data["max_orders_per_minute"]),
            # The API return this as an array, where the first element
            # is the amount and the second is the currency code.
            # We save each value separately for easy managment.
            min_order_amount_value=Decimal(
                market_data["minimum_order_amount"][0],
            ),
            min_order_amount_currency=market_data["minimum_order_amount"][1],
            taker_fee=Decimal(market_data["taker_fee"]),
            taker_discount_percentage=Decimal(
                market_data["taker_discount_percentage"],
            ),
            maker_fee=Decimal(market_data["maker_fee"]),
            maker_discount_percentage=Decimal(
                market_data["maker_discount_percentage"],
            ),
        )
        return market

    @classmethod
    def get_all_markets(cls) -> list:
        """
        Retrieves all markets available on Buda.com API.

        :returns: A list of markets.
        :rtype: list[Market]
        """
        endpoint = "/markets"
        markets = []
        markets_data = fetch_data(endpoint)["markets"]

        for market_data in markets_data:
            markets.append(cls.create("", market_data))

        return markets

    class Meta:
        managed = False


class Ticker(models.Model):
    """
    A class that stores all data returned from
    `/markets/{market_id}/ticker` Buda.com API endpoint.

    USAGE
    >>> ticker = Ticker.create(market_id: str)
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

    @classmethod
    def create(cls, market_id: str):
        """
        Custom method to initialize a :class:`Ticker` instance.

        :param str market_id: valid market identifier, e.g. `btc-clp`.
        :rtype: Ticker
        """
        # retrieve the ticket for the specific market
        endpoint = f"/markets/{market_id}/ticker"
        ticker_data = fetch_data(endpoint)["ticker"]  # TODO: ?

        # create the instance
        ticker = cls(
            market_id=ticker_data["market_id"],
            price_variation_24h=Decimal(ticker_data["price_variation_24h"]),
            price_variation_7d=Decimal(ticker_data["price_variation_7d"]),
            # The API return all figures as an array, where the first
            # element is the amount and the second is the currency code.
            # We save each value separately for easy managment.
            last_price_value=Decimal(ticker_data["last_price"][0]),
            last_price_currency=ticker_data["last_price"][1],
            max_bid_value=Decimal(ticker_data["max_bid"][0]),
            max_bid_currency=ticker_data["max_bid"][1],
            min_ask_value=Decimal(ticker_data["min_ask"][0]),
            min_ask_currency=ticker_data["min_ask"][1],
            volume_value=Decimal(ticker_data["volume"][0]),
            volume_currency=ticker_data["volume"][1],
        )
        return ticker

    class Meta:
        managed = False


class Spread(models.Model):
    """
    A class that calculates the current spread of a given market.

    USAGE
    >>> spread = Spread.create(market_id: str)
    """

    market_id = models.CharField(max_length=30)
    value = models.DecimalField(max_digits=22, decimal_places=10)
    currency = models.CharField(max_length=15)
    fetch_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, market_id: str):
        """
        Custom method to initialize a :class:`Spread` instance.

        :param str market_id: valid market identifier, e.g. `btc-clp`.
        :rtype: Spread
        """
        # get the ticker for the given market
        ticker = Ticker.create(market_id)

        # create the instance
        spread = cls(
            market_id=ticker.market_id,
            value=ticker.min_ask_value - ticker.max_bid_value,
            currency=ticker.max_bid_currency,
        )
        return spread

    @classmethod
    def get_each_markets_spread(cls) -> list:
        """
        Calculates the spread for all markets available on Buda.com API.

        :returns: A list of spreads.
        :rtype: list[Spread]
        """
        spreads = []
        markets = Market.get_all_markets()
        for market in markets:
            spreads.append(Spread.create(market.id))
        return spreads


class Polling(models.Model):
    """
    A class that represent a comparison between
    the current and a stored spread of a market.

    USAGE
    >>> polling = Polling.create(stored: Spread)
    """

    market_id = models.CharField(max_length=30)
    current_is_greater = models.BooleanField()
    stored_is_greater = models.BooleanField()
    difference = models.DecimalField(
        max_digits=22,
        decimal_places=10,
    )

    # current spread data
    current_spread_currency = models.CharField(max_length=15)
    current_spread_value = models.DecimalField(
        max_digits=22,
        decimal_places=10,
    )

    # stored spread data
    stored_spread_date = models.DateTimeField()
    stored_spread_currency = models.CharField(max_length=15)
    stored_spread_value = models.DecimalField(
        max_digits=22,
        decimal_places=10,
    )

    fetch_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, stored: Spread):
        """
        Custom method to initialize a :class:`Polling` instance.

        :param Spread stored: a spread already calculated
        to compare with the current one.
        :rtype: Polling
        """
        # retrieve the current spread for the same market of the given one
        current = Spread.create(stored.market_id)

        # create the instance
        polling = cls(
            market_id=current.market_id,
            current_is_greater=True if current.value > stored.value else False,
            stored_is_greater=True if current.value < stored.value else False,
            difference=abs(current.value - stored.value),
            current_spread_value=current.value,
            current_spread_currency=current.currency,
            stored_spread_value=stored.value,
            stored_spread_currency=stored.currency,
            stored_spread_date=stored.fetch_date,
        )
        return polling

    class Meta:
        managed = False
