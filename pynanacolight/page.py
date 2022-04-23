# -*- coding: utf-8 -*-
"""
ページの抽象レベル操作を行う
"""
from requests import Session
from pynanacolight.parser import (
    InputTagParser,
    AnchorTagParser,
    TitleParser,
    MenuPageBalanceParser,
)
from pynanacolight.util import logging

BASE_URL = "https://www.nanaco-net.jp/pc/emServlet"

ENCODING = "shift_jis"

# nanaco-netのサイトでデフォルトで取得対象にするinputタグ
DEFAULT_INPUT_DATA_NAMES = [
    "_PageID",
    "_DataStoreID",
    "_SeqNo",
    "_ControlID",
    "_WID",
    "_ORGWID",
    "_WIDManager",
    "_preProcess",
    "_TimeOutControl",
    "_WIDMode",
    "_WindowName",
    "_ReturnPageInfo",
]


class LoginPage:
    """login page controller
    """

    def __init__(self, session: Session):
        self._session = session

        html = self._session.get(BASE_URL)
        html.encoding = ENCODING

        parser = InputTagParser()
        parser.feed(html.text)

        self.data = {k: v for k, v in parser.data.items()
                     if k in DEFAULT_INPUT_DATA_NAMES}

    @logging
    def input_nanaco_number(self, nanaco_number):
        self.data.update({"XCID": nanaco_number})

    @logging
    def input_security_code(self, security_code):
        self.data.update({"SECURITY_CD": security_code})

    @logging
    def input_password(self, password):
        self.data.update({"LOGIN_PWD": password})

    @logging
    def click_login_by_card_number(self):
        self.data.update({"ACT_ACBS_do_LOGIN2": ""})

        html = self._session.post(BASE_URL, self.data)
        html.encoding = ENCODING
        return html

    @logging
    def click_login_by_password(self):
        self.data.update({"ACT_ACBS_do_LOGIN1": ""})

        html = self._session.post(BASE_URL, self.data)
        html.encoding = ENCODING
        return html


class MenuPage:
    """menu page controller
    """

    def __init__(self, session: Session, html):
        self._session = session

        parser = AnchorTagParser()
        parser.feed(html.text)

        self.data = {
            "_SeqNo": parser.anchors[0]["_SeqNo"][0],
            "_DataStoreID": parser.anchors[0]["_DataStoreID"][0]
        }

        self.balance_card = None
        self.balance_center = None

        parser = MenuPageBalanceParser()
        parser.feed(html.text)

        self.balance_card = parser.balance_card
        self.balance_center = parser.balance_center

        self.balance_card_timestamp = parser.balance_card_timestamp
        self.balance_center_timestamp = parser.balance_center_timestamp

        self.can_credit_charge = None

    @logging
    def click_login_credit_charge(self):
        self.data.update(
            {
                "_ActionID": "ACBS_do_CRDT_TRADE_MENU",
                "_ControlID": "BS_PCB0000_Control",
                "_PageID": "SCBS_PCB8001",
            }
        )
        html = self._session.get(BASE_URL, self.data)
        html.encoding = ENCODING

        parser = TitleParser()
        parser.feed(html.text)

        if parser.title == "nanaco / クレジットチャージ　パスワード認証画面":
            self.can_credit_charge = True
        elif parser.title == "nanaco / クレジットチャージ・オートチャージのご案内":
            self.can_credit_charge = False

        return html

    @logging
    def click_register_gift(self):
        self.data.update(
            {
                "_ActionID": "ACBS_do_NNC_GIFT_REG",
                "_ControlID": "BS_PCB1101_Control",
                "_PageID": "SCBS_PCB1101",
            }
        )

        html = self._session.get(BASE_URL, params=self.data)
        html.encoding = ENCODING
        return html

    # @property
    # def text_balance_card(self):
    #     return self.balance_card

    # @property
    # def text_balance_center(self):
    #     return self.balance_center

    # @property
    # def text_balance_card_timestamp(self):
    #     return self.balance_card_timestamp

    # @property
    # def text_balance_center_timestamp(self):
    #     return self.balance_center_timestamp

    # @property
    # def can_credit_charge(self):
    #     return self.can_credit_charge
