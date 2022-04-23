# -*- coding: utf-8 -*-
"""
ページの抽象レベル操作を行う
"""
from requests import Session
from dataclasses import dataclass
from datetime import datetime

from pynanacolight.page import ENCODING
from pynanacolight.parser import (
    InputTagParser,
    GiftIDInputPageValidationParser,
    GiftIDConfirmPageParser,
    GiftIDRegistrationResultPageParser,
)
from pynanacolight.util import logging, logger
from pynanacolight.exception import InvalidGiftIDException


@dataclass
class NanacoGift:
    """Nanaco gift ID data class.
    """
    has_registered: bool
    charged_nanaco_number: str
    gift_id: str
    amount: int
    receipt_number: str
    receivable_date: datetime


class GiftIDRegistrationPage:
    """nanaco / nanacoギフト登録
    """

    def __init__(self, session: Session, html):
        self._session = session

        parser = InputTagParser()
        parser.feed(html.text)

        # postメソッドで投げるパラメータ
        INPUT_DATA_NAMES = ["no", "date", "sig", "ver", "gid"]

        self.data = {k: v for k, v in parser.data.items()
                     if k in INPUT_DATA_NAMES}

    @logging
    def click_accept_and_register(self):
        URL = "https://nanacogift.jp/ap/p/top.do"
        html = self._session.post(URL, self.data)
        html.encoding = ENCODING
        return html


class GiftIDInputPage:
    """ギフトID登録フォーム(register1)

    Returns:
        _type_: _description_
    """

    def __init__(self, session: Session, html):
        self._session = session

        self.gift_has_registered = False
        self.gift_amount = None
        self.gift_receipt_number = None
        self.gift_receivable_date = None

        INPUT_DATA_NAMES = ["vsid"]

        parser = InputTagParser()
        parser.feed(html.text)
        self.data = {k: v for k, v in parser.data.items()
                     if k in INPUT_DATA_NAMES}

    @logging
    def input_code(self, gift_id):
        self.gift_id = gift_id
        self.data.update(
            {
                "id1": gift_id[0:4],
                "id2": gift_id[4:8],
                "id3": gift_id[8:12],
                "id4": gift_id[12:16],
            }
        )

    @logging
    def click_goto_confirm_page(self):
        """click confirm page and validate gift id
        確認画面へ　をクリック

        Returns:
            _type_: _description_
        """
        URL = "https://nanacogift.jp/ap/p/register2.do"
        html = self._session.post(URL, self.data)
        html.encoding = ENCODING

        try:
            self._validate_gift_id(html)
        except InvalidGiftIDException as e:
            logger.error("Invalid Gift ID")
            raise e

        # 登録済みの確認
        parser = GiftIDRegistrationResultPageParser()
        parser.feed(html.text)

        self.gift_has_registered = parser.gift_has_registered

        if self.gift_has_registered:
            self.gift_amount = parser.gift_amount
            self.gift_receipt_number = parser.gift_receipt_number
            self.gift_receivable_date = parser.gift_receivable_date
        else:
            self.gift_receipt_number = None
            self.gift_receivable_date = None

        # debug
        msg_true = "登録済みです"
        msg_false = "登録されていません"

        logger.info(
            msg_true if self.gift_has_registered else msg_false)

        return html

    def _validate_gift_id(self, html):
        parser = GiftIDInputPageValidationParser()
        parser.feed(html.text)

        if not parser.is_valid_gift_id:
            raise InvalidGiftIDException()


class GiftIDConfirmPage:
    """ギフトID登録内容確認(register3)

    Raises:
        InvalidGiftcodeException: 無効なギフトコードが入力された場合
        GiftcodeAlreadyRegisteredException: 既に登録済みのギフトコードが入力された場合

    Returns:
        _type_: _description_
    """

    def __init__(self, session: Session, html):
        self._session = session

        self.gift_has_registered = False
        self.gift_amount = None
        self.gift_receipt_number = None
        self.gift_receivable_date = None

        parser = InputTagParser()
        parser.feed(html.text)

        INPUT_DATA_NAMES = ["vsid", "sessToken"]

        self.data = {k: v for k, v in parser.data.items()
                     if k in INPUT_DATA_NAMES}

        parser = GiftIDRegistrationResultPageParser()
        parser.feed(html.text)

        self.gift_has_registered = parser.gift_has_registered

        if self.gift_has_registered:
            # 登録済みの場合
            self.gift_amount = parser.gift_amount
            self.gift_receipt_number = parser.gift_receipt_number
            self.gift_receivable_date = parser.gift_receivable_date

        else:
            # 未登録の場合
            parser = GiftIDConfirmPageParser()
            parser.feed(html.text)

            self.gift_amount = parser.gift_amount
            self.gift_receipt_number = None
            self.gift_receivable_date = None

    # def _has_registered(self, html):
    #     parser = GiftIDRegistrationResultPageParser()
    #     parser.feed(html.text)
    #     return parser.gift_has_registered

    # @property
    # def gift_amount(self):
    #     return self._gift_amount

    # @property
    # def gift_has_registered(self):
    #     return self._gift_has_registered

    # @property
    # def gift_receipt_number(self):
    #     return self._gift_receipt_number

    # @property
    # def gift_receivable_date(self):
    #     return self._gift_receivable_date

    @logging
    def click_register(self):
        URL = "https://nanacogift.jp/ap/p/register4.do"
        html = self._session.post(URL, self.data)
        html.encoding = ENCODING
        return html


class GiftIDRegistrationResultPage:
    """ギフトID登録完了(register5)

    https://nanacogift.jp/ap/p/register5.do?vsid=YL02yQjprlyju7i_7BkNzkfE-IIKL6lw%211979915677%211650186586345

    """

    def __init__(self, session: Session, html):
        self._session = session

        parser = GiftIDRegistrationResultPageParser()
        parser.feed(html.text)
        # self._parser = parser

        # parser = GiftAmountParser()
        # parser.feed(html.text)

        self.gift_amount = parser.gift_amount
        self.gift_has_registered = parser.gift_has_registered
        self.gift_receivable_date = parser.gift_receivable_date
        self.gift_receipt_number = parser.gift_receipt_number

    # @property
    # def gift_amount(self):
    #     return self._parser.gift_amount

    # @property
    # def gift_has_registered(self):
    #     return self._parser.gift_has_registered

    # @property
    # def gift_receipt_number(self):
    #     return self._parser.gift_receipt_number

    # @property
    # def gift_receivable_date(self):
    #     return self._parser.gift_receivable_date
