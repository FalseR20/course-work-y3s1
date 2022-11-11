import logging

CUSTOM_LOG_LEVEL = logging.DEBUG + 5

logging.addLevelName(CUSTOM_LOG_LEVEL, "PROJECT")
logging.basicConfig(level=CUSTOM_LOG_LEVEL)
