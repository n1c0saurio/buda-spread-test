from .test_setup import TestSetUp
from django.urls import reverse
from rest_framework import status


class TestViews(TestSetUp):
    """
    Tests for `/spreads/` endpoint.
    """

    def test_get_market_spread(self):
        """
        Validate correct spread retrieving.
        """
        url = reverse("spread-detail", kwargs={"pk": self.valid_market_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
