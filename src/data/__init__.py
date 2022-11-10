import pickle
from pathlib import Path
from typing import Final, List

_DATA_PATH: Final = Path(__file__).resolve().parent
_BASE_CURRENCIES_PATH: Final = _DATA_PATH / "base_currencies.pkl"
_CRYPTO_CURRENCIES_PATH: Final = _DATA_PATH / "crypto_currencies.pkl"

with _BASE_CURRENCIES_PATH.open("rb") as file:
    BASE_CURRENCIES: List[str] = pickle.load(file)

with _CRYPTO_CURRENCIES_PATH.open("rb") as file:
    CRYPTO_CURRENCIES: List[str] = pickle.load(file)

if __name__ == "__main__":
    print(f"{BASE_CURRENCIES=}")
    print(f"{CRYPTO_CURRENCIES=}")
