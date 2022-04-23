# -*- coding: utf-8 -*-
import logging
from logging import getLogger, StreamHandler, Formatter
from pynanacolight.parser import InputTagParser
from requests import session

LOG_LEVEL = logging.DEBUG

logger = getLogger(__name__)
logger.setLevel(LOG_LEVEL)
stream_handler = StreamHandler()
stream_handler.setLevel(LOG_LEVEL)

handler_format = Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(handler_format)

logger.addHandler(stream_handler)


# logging decorator
def logging(func):
    def wrapper(*args, **kwargs):
        logger.debug(func.__qualname__ + str(args) + str(kwargs))
        res = func(*args, **kwargs)
        return res

    return wrapper


def analyze(url):
    s = session()
    html = s.get(url=url)
    parser = InputTagParser()
    parser.feed(html.text)
