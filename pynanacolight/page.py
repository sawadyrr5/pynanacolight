# -*- coding: utf-8 -*-
"""
ページの抽象レベル操作を行う
"""
from requests import session
from urllib.parse import urlencode

from pynanacolight.parser import InputTagParser, AnchorTagParser, BalanceParser
from pynanacolight.util.logger import logging

BASE_URL = 'https://www.nanaco-net.jp/pc/emServlet'

ENCODING = 'shift_jis'

DEFAULT_INPUT_DATA_NAMES = [
    "_PageID", "_DataStoreID", "_SeqNo", "_ControlID", "_WID", "_ORGWID", "_WIDManager", "_preProcess",
    "_TimeOutControl", "_WIDMode", "_WindowName", "_ReturnPageInfo"]


# Internal
@logging
def _post(session: session(), url: str, data: dict):
    html = session.post(url, data)
    html.encoding = ENCODING
    return html


# Internal
@logging
def _get(session: session(), url: str, param: dict):
    _url = url + '?' + urlencode(param)
    html = session.get(_url)
    html.encoding = ENCODING
    return html


class LoginPage:
    def __init__(self, session: session()):
        self._session = session
        html = self._session.get(BASE_URL)

        parser = InputTagParser()
        parser.feed(html.text)

        wanted_keys = DEFAULT_INPUT_DATA_NAMES
        self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}

    @logging
    def input_nanaco_number(self, nanaco_number):
        self.data.update(
            {
                "XCID": nanaco_number
            }
        )

    @logging
    def input_card_number(self, card_number):
        self.data.update(
            {
                "SECURITY_CD": card_number
            }
        )

    @logging
    def click_login(self):
        self.data.update(
            {
                "ACT_ACBS_do_LOGIN2": ''
            }
        )

        html = _post(
            session=self._session,
            url=BASE_URL,
            data=self.data
        )
        return html


class MenuPage:

    def __init__(self, session: session(), html):
        self._session = session

        parser = AnchorTagParser()
        parser.feed(html.text)

        # prepare parameter
        self.data = {}
        self.data.update({"_SeqNo": parser.anchors[0]['_SeqNo'][0]})
        self.data.update({"_WBSessionID": parser.anchors[0]['_WBSessionID'][0]})
        self.data.update({"_DataStoreID": parser.anchors[0]['_DataStoreID'][0]})

        self._balance_card = None
        self._balance_center = None

        # read balance
        parser = BalanceParser()
        parser.feed(html.text)

        self._balance_card = parser.balance_card
        self._balance_center = parser.balance_center

    @logging
    def click_login_credit_charge(self):
        self.data.update(
            {
                "_ActionID": 'ACBS_do_CRDT_TRADE_MENU',
                "_ControlID": 'BS_PCB0000_Control',
                "_PageID": 'SCBS_PCB8001'
            }
        )

        html = _get(
            session=self._session,
            url=BASE_URL,
            param=self.data
        )
        return html

    @logging
    def click_register_gift(self):
        self.data.update(
            {
                "_ActionID": 'ACBS_do_NNC_GIFT_REG',
                "_ControlID": 'BS_PCB0000_Control',
                "_PageID": 'SCBS_PCB1111'
            }
        )

        html = _get(
            session=self._session,
            url=BASE_URL,
            param=self.data
        )
        return html

    @property
    def text_balance_card(self):
        return self._balance_card

    @property
    def text_balance_center(self):
        return self._balance_center
