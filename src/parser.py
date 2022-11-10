import datetime
from typing import List, Tuple

from coinbase.wallet.client import Client

client = Client("api_key", "api_secret")  # key and secret are not required for prices parsing


def parse_dataset(currency_pair: str) -> Tuple[List[float], List[float]]:
    prices = client.get_historic_prices(currency_pair=currency_pair, period="hour")["prices"]
    dataset: List[float] = [float(price["price"]) for price in prices]
    dataset_datetimes = [datetime.datetime.strptime(price["time"], "%Y-%m-%dT%H:%M:%SZ") for price in prices]
    last_time = dataset_datetimes[-1]
    dataset_times: List[float] = [(last_time - dataset_dt).total_seconds() / 60 for dataset_dt in dataset_datetimes]

    # import pickle
    # from src.data import _DATA_PATH
    # with _DATA_PATH.joinpath("data.pkl").open("wb") as file:
    #     pickle.dump((dataset, dataset_times), file)

    # import pickle
    #
    # from src.data import _DATA_PATH
    #
    # with _DATA_PATH.joinpath("data.pkl").open("rb") as file:
    #     (dataset, dataset_times) = pickle.load(file)

    return dataset, dataset_times
