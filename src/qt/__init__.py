import logging

logging.addLevelName(lvl := logging.DEBUG + 5, "qt")
logging.basicConfig(level=lvl)
