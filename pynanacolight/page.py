# -*- coding: utf-8 -*-
"""
ページの抽象レベル操作を行う
"""
from requests import session
from urllib.parse import urlencode

from pynanacolight.parser import InputTagParser, AnchorTagParser, BalanceParser

import logging
from logging import getLogger, StreamHandler, Formatter

_LOGLEVEL = logging.DEBUG

logger = getLogger(__name__)
logger.setLevel(_LOGLEVEL)
stream_handler = StreamHandler()
stream_handler.setLevel(_LOGLEVEL)

handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)

logger.addHandler(stream_handler)

BASE_URL = 'https://www.nanaco-net.jp/pc/emServlet'
REGISTER_GIFT_URL = 'https://nanacogift.jp/ap/p/top.do'
REGISTER_GIFT_SUBMIT_URL = 'https://nanacogift.jp/ap/p/register2.do'
REGISTER_GIFT_CONFIRM_URL = 'https://nanacogift.jp/ap/p/register4.do'

ENCODING = 'shift_jis'

DEFAULT_INPUT_DATA = [
    "_PageID", "_DataStoreID", "_SeqNo", "_ControlID", "_WID", "_ORGWID", "_WIDManager", "_preProcess",
    "_TimeOutControl", "_WIDMode", "_WindowName", "_ReturnPageInfo"]


class LoginPage:
    def __init__(self, session: session()):
        self._session = session
        html = self._session.get(BASE_URL)

        parser = InputTagParser()
        parser.feed(html.text)

        names = DEFAULT_INPUT_DATA
        self.data = {k: v for k, v in parser.data.items() if k in names}

    def input_nanaco_number(self, nanaco_number):
        data = {
            "XCID": nanaco_number
        }
        self.data.update(data)

        logger.info("input_nanaco_number: " + str(data))

    def input_card_number(self, card_number):
        data = {
            "SECURITY_CD": card_number
        }
        self.data.update(data)

        logger.info("input_card_number: " + str(data))

    def click_login(self):
        data = {
            "ACT_ACBS_do_LOGIN2": ''
        }
        self.data.update(data)

        url = BASE_URL
        data = self.data

        logger.info("click_login: " + str(data))

        html = self._session.post(url, data)
        html.encoding = ENCODING

        return html


class MenuPage:
    _DATA_CREDIT_CHARGE_LOGIN = {
        "_ActionID": 'ACBS_do_CRDT_TRADE_MENU',
        "_ControlID": 'BS_PCB0000_Control',
        "_PageID": 'SCBS_PCB8001'
    }

    _DATA_REGISTER_GIFT = {
        "_ActionID": 'ACBS_do_NNC_GIFT_REG',
        "_ControlID": 'BS_PCB0000_Control',
        "_PageID": 'SCBS_PCB1111'
    }

    def __init__(self, session: session(), html):
        self._session = session
        self._html = html

        parser = AnchorTagParser()
        parser.feed(html.text)

        # prepare parameter
        self.data = {}
        self.data.update({"_SeqNo": parser.anchors[0]['_SeqNo'][0]})
        self.data.update({"_WBSessionID": parser.anchors[0]['_WBSessionID'][0]})
        self.data.update({"_DataStoreID": parser.anchors[0]['_DataStoreID'][0]})

        self._balance_card = None
        self._balance_center = None

        self._read_balance(html)

    def _read_balance(self, html):
        parser = BalanceParser()
        parser.feed(html.text)

        self._balance_card = parser.amount[0]
        self._balance_center = parser.amount[1]

    def click_login_credit_charge(self):
        self.data.update(self.__class__._DATA_CREDIT_CHARGE_LOGIN)

        qs = urlencode(self.data)
        url = BASE_URL + '?' + qs

        logger.info("click_login_credit_charge: " + str(url))

        html = self._session.get(url)
        html.encoding = ENCODING

        return html

    def click_register_gift(self):
        self.data.update(self.__class__._DATA_REGISTER_GIFT)

        qs = urlencode(self.data)
        url = BASE_URL + '?' + qs

        logger.info("click_register_gift: " + str(url))

        html = self._session.get(url)
        html.encoding = ENCODING

        return html

    @property
    def text_balance_card(self):
        return self._balance_card

    @property
    def text_balance_center(self):
        return self._balance_center


# Internal
def _post(session: session(), url: str, data: dict):
    html = session.post(url, data)
    html.encoding = ENCODING

    logger.info(str(url) + str(data))
    return html
