"""Utility module for Buda.com API consumption."""

import requests

BASE_URL = "https://www.buda.com/api"
VERSION = "/v2"


def fetch_data(endpoint: str) -> dict:
    """
    Get data from Buda API.

    :param str endpoint: valid endpoint to retrieve data from.
    :returns: A dictionary with the response data.
    :rtype: dict
    """
    url = BASE_URL + VERSION + endpoint
    response = requests.get(url)

    # throw an HTTPError if the request wasn't succesful
    response.raise_for_status()

    return response.json()
