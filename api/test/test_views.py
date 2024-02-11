from .test_setup import TestSetUp
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from ..models import Spread


class TestViews(TestSetUp):
    """
    Tests for `/spreads/*` endpoints.
    """

    def test_get_each_markets_spread(self):
        """
        Validate correct spreads list retrieving.
        """
        url = reverse("spread-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["content-type"], "application/json")

    def test_get_market_spread(self):
        """
        Validate correct spread retrieving.
        """
        url = reverse(
            "spread-detail",
            kwargs={"market_id": self.valid_market_id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["content-type"], "application/json")

    def test_save_spread(self):
        """
        Validate if a spread is saved on database
        """
        url = reverse(
            "spread-save",
            kwargs={"market_id": self.valid_market_id},
        )
        response = self.client.get(url)

        # find a spread with the same value as the response data
        spread_value = Decimal(response.json()["value"])
        spread_saved = Spread.objects.get(value=spread_value)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(spread_saved)

    def test_get_polling_before_saving_a_spread(self):
        """
        Validate polling request without spreads stored.
        """
        url = reverse(
            "spread-polling",
            kwargs={"market_id": self.valid_market_id},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_polling_after_saving_a_spread(self):
        """
        Validate polling request with a spread stored.
        """
        save_spread_url = reverse(
            "spread-save",
            kwargs={"market_id": self.valid_market_id},
        )
        self.client.get(save_spread_url)

        polling_url = reverse(
            "spread-polling",
            kwargs={"market_id": self.valid_market_id},
        )
        polling_response = self.client.get(polling_url)

        self.assertEqual(polling_response.status_code, status.HTTP_200_OK)
        self.assertEqual(polling_response["content-type"], "application/json")
