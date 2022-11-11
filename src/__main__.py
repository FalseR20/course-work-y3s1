import logging

from src import CUSTOM_LOG_LEVEL
from src.qt.app import app


def main():
    app.exec()


if __name__ == "__main__":
    logging.basicConfig(level=CUSTOM_LOG_LEVEL)
    main()
