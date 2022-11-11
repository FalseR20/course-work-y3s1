import datetime
from typing import List, Tuple

from coinbase.wallet.client import Client

client = Client("api_key", "api_secret")  # key and secret are not required for prices parsing

counter: int = 1


def parse_dataset(currency_pair: str) -> Tuple[List[float], List[datetime.datetime]]:
    global counter
    if counter == 0:
        import pickle

        from src.data import _DATA_PATH

        with _DATA_PATH.joinpath("data.pkl").open("rb") as file:
            (dataset, dataset_datetimes) = pickle.load(file)

    if counter > 0:
        prices = client.get_historic_prices(currency_pair=currency_pair, period="hour")["prices"]
        dataset: List[float] = [float(price["price"]) for price in prices]
        dataset_datetimes = [datetime.datetime.strptime(price["time"], "%Y-%m-%dT%H:%M:%SZ") for price in prices]
        dataset.reverse()
        dataset_datetimes.reverse()

    print(counter)
    counter += 1

    # import pickle
    # from src.data import _DATA_PATH
    # with _DATA_PATH.joinpath("data.pkl").open("wb") as file:
    #     pickle.dump((dataset, dataset_datetimes), file)

    # import pickle
    #
    # from src.data import _DATA_PATH
    #
    # with _DATA_PATH.joinpath("data.pkl").open("rb") as file:
    #     (dataset, dataset_datetimes) = pickle.load(file)

    return dataset, dataset_datetimes
