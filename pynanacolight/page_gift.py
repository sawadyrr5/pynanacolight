# -*- coding: utf-8 -*-
"""
ページの抽象レベル操作を行う
"""
from requests import session

from pynanacolight.parser import InputTagParser
from pynanacolight.page import ENCODING, logger


REGISTER_GIFT_URL = 'https://nanacogift.jp/ap/p/top.do'
REGISTER_GIFT_SUBMIT_URL = 'https://nanacogift.jp/ap/p/register2.do'
REGISTER_GIFT_CONFIRM_URL = 'https://nanacogift.jp/ap/p/register4.do'


class RegisterGiftPage:

    def __init__(self, session: session(), html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        names = ["no", "date", "sig", "ver", "gid"]
        self.data = {k: v for k, v in parser.data.items() if k in names}

    def click_accept(self):
        url = REGISTER_GIFT_URL
        data = self.data

        logger.info("click accept: " + str(data))

        html = self._session.post(url, data)
        html.encoding = ENCODING

        return html


class RegisterGiftCodeInputPage:

    def __init__(self, session: session(), html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        names = ["vsid"]
        self.data = {k: v for k, v in parser.data.items() if k in names}

    def input_code(self, code):
        data = {
            "id1": code[0: 4],
            "id2": code[4: 8],
            "id3": code[8:12],
            "id4": code[12:16]
        }
        self.data.update(data)

        logger.info("input_charge_amount: " + str(data))

    def click_submit(self):
        url = REGISTER_GIFT_SUBMIT_URL
        data = self.data

        logger.info("click_submit: " + str(data))

        html = self._session.post(url, data)
        html.encoding = ENCODING

        return html


class RegisterGiftCodeConfirmPage:

    def __init__(self, session: session(), html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        names = ["vsid"]
        self.data = {k: v for k, v in parser.data.items() if k in names}

    def click_confirm(self):
        url = REGISTER_GIFT_CONFIRM_URL
        data = self.data

        logger.info("click_confirm: " + str(data))

        html = self._session.post(url, data)
        html.encoding = ENCODING

        return html