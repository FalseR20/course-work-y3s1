from typing import List

from coinbase.wallet.client import Client

client = Client("api_key", "api_secret")  # key and secret are not required for prices parsing
base_currencies: List[dict] = client.get_currencies()["data"]
