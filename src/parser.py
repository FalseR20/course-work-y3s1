import datetime
import logging
from typing import List, Tuple

from coinbase.wallet.client import Client

from src import CUSTOM_LOG_LEVEL

_CLIENT = Client("api_key", "api_secret")  # key and secret are not required for prices parsing


def parse_dataset(currency_pair: str) -> Tuple[List[float], List[datetime.datetime]]:
    prices = _CLIENT.get_historic_prices(currency_pair=currency_pair, period="hour")["prices"]
    dataset: List[float] = [float(price["price"]) for price in prices]
    dataset_datetimes = [
        datetime.datetime.strptime(price["time"], "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=3)
        for price in prices
    ]
    dataset.reverse()
    dataset_datetimes.reverse()
    logging.log(CUSTOM_LOG_LEVEL, f"parse_dataset: {dataset=}")
    logging.log(CUSTOM_LOG_LEVEL, f"parse_dataset: {dataset_datetimes=}")
    return dataset, dataset_datetimes
