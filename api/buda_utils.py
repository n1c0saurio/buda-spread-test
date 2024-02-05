"""Utility module for Buda.com API consumption."""

import requests

BASE_URL = "https://www.buda.com/api"
VERSION = "/v3"


def fetch_data(endpoint: str) -> dict | list:
    """
    Get data from Buda API.

    Parameter
    ---------
    endpoint : str
        Valid endpoint to retrieve data from.

    Return
    ------
    dict | list
        Either a dictionary or a list of dictionaries with the response data.
    """
    url = f"{BASE_URL}{VERSION}{endpoint}"
    response = requests.get(url)
    return response.json()
