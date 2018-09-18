# -*- coding: utf-8 -*-
"""
ページの抽象レベル操作を行う
"""
from requests import session

from pynanacolight.page import _post
from pynanacolight.parser import InputTagParser
from pynanacolight.util.logger import logging


class RegisterGiftPage:
    INPUT_DATA_NAMES = ["no", "date", "sig", "ver", "gid"]

    URL = 'https://nanacogift.jp/ap/p/top.do'

    def __init__(self, session: session(), html):
        self._session = session

        parser = InputTagParser()
        parser.feed(html.text)

        wanted_keys = self.__class__.INPUT_DATA_NAMES
        self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}

    @logging
    def click_accept(self):
        html = _post(
            session=self._session,
            url=self.__class__.URL,
            data=self.data
        )
        return html


class RegisterGiftCodeInputPage:
    INPUT_DATA_NAMES = ["vsid"]

    URL = 'https://nanacogift.jp/ap/p/register2.do'

    def __init__(self, session: session(), html):
        self._session = session

        parser = InputTagParser()
        parser.feed(html.text)

        wanted_keys = self.__class__.INPUT_DATA_NAMES
        self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}

    @logging
    def input_code(self, code):
        data = {
            "id1": code[0: 4],
            "id2": code[4: 8],
            "id3": code[8:12],
            "id4": code[12:16]
        }
        self.data.update(data)

    @logging
    def click_submit(self):
        html = _post(
            session=self._session,
            url=self.__class__.URL,
            data=self.data
        )
        return html


class RegisterGiftCodeConfirmPage:
    INPUT_DATA_NAMES = ["vsid"]

    URL = 'https://nanacogift.jp/ap/p/register4.do'

    def __init__(self, session: session(), html):
        self._session = session

        parser = InputTagParser()
        parser.feed(html.text)

        wanted_keys = self.__class__.INPUT_DATA_NAMES
        self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}

    @logging
    def click_confirm(self):
        html = _post(
            session=self._session,
            url=self.__class__.URL,
            data=self.data
        )
        return html
