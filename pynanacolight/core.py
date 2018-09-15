# -*- coding: utf-8 -*-
from pynanacolight.page import *

import logging
from logging import getLogger, StreamHandler, Formatter

from pynanacolight.page_creditcharge import CreditChargePasswordAuthPage, CreditChargeMenuPage, CreditChargeInputPage, \
    CreditChargeConfirmPage, CreditChargeCancelPage, CreditChargeCancelConfirmPage
from pynanacolight.page_gift import RegisterGiftPage, RegisterGiftCodeInputPage, RegisterGiftCodeConfirmPage

_LOGLEVEL = logging.DEBUG

logger = getLogger(__name__)
logger.setLevel(_LOGLEVEL)
stream_handler = StreamHandler()
stream_handler.setLevel(_LOGLEVEL)

handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)

logger.addHandler(stream_handler)


# class PyNanacoLight:
#
#     def __init__(self, session):
#
#         self._session = session
#
#         self._balance_card = None
#         self._balance_center = None
#
#         self._charge_count = None
#         self._charge_amount = None
#         self._registerd_credit_card = None
#
#         self.page = None
#
#     def login(self, nanaco_number, card_number):
#         # self.nanaco_number = nanaco_number
#         # self.card_number = card_number
#
#         self.page = LoginPage()
#         self.page.input_nanaco_number(nanaco_number)
#         self.page.input_card_number(card_number)
#         self.page = self.page.click_login()
#
#         logger.info("login: " + nanaco_number + " " + card_number)
#
#         self._balance_card = self.page.balance_card
#         self._balance_center = self.page.balance_center
#
#         logger.info("balance_card: " + self.balance_card)
#         logger.info("balance_center: " + self.balance_center)
#
#     def login_credit_charge(self, password):
#         self.page = MenuPage()
#         self.page = self.page.login_credit_charge(password)
#
#         if isinstance(self.page, CCMenuPage):
#             logger.info("login credit charge succeed")
#
#             self.page = CCHistoryPage()
#
#             self._registerd_credit_card = self.page.registered_credit_card
#             self._charge_amount = self.page.charge_amount
#             self._charge_count = self.page.charge_count
#
#             logger.info("registered credit card: " + self._registerd_credit_card if self._registerd_credit_card else '')
#             logger.info("charge count: " + self.charge_count if self.charge_count else '')
#             logger.info("charge amount: " + self.charge_amount if self.charge_amount else '')
#         else:
#
#             logger.info("login credit charge failed")
#
#     def charge(self, amount):
#         self.page = CCMenuPage()
#         self.page.charge(amount)
#
#     def release(self, password):
#         self.page = CCMenuPage()
#         self.page.release(password)
#
#     def register_giftcode(self):
#         self.page = CCMenuPage()
#         self.page.register_gift()
#
#     @property
#     def balance_card(self):
#         return self._balance_card
#
#     @property
#     def balance_center(self):
#         return self._balance_center
#
#     @property
#     def registered_credit_card(self):
#         return self._registerd_credit_card
#
#     @property
#     def charge_count(self):
#         return self._charge_count
#
#     @property
#     def charge_amount(self):
#         return self._charge_amount


from requests import session


class PyNanacoLight:
    def __init__(self, session: session()):
        self._session = session

        self.page = None
        self.html = None

        self.balance_card = 0
        self.balance_center = 0

        self.credit_charge_password = ''

    def login(self, nanaco_number, card_number):
        page = LoginPage(self._session)

        page.input_nanaco_number(nanaco_number)
        page.input_card_number(card_number)

        try:
            self.html = page.click_login()
        except:
            pass

        page = MenuPage(self._session, self.html)
        self.balance_card = page.text_balance_card
        self.balance_center = page.text_balance_center

    # def _read_balance(self):
    #     page = MenuPage2(self._session, self.html)
    #     self.balance_card = page.text_balance_card
    #     self.balance_center = page.text_balance_center

    def login_credit_charge(self, password):
        self.credit_charge_password = password

        page = MenuPage(self._session, self.html)
        self.html = page.click_login_credit_charge()

        page = CreditChargePasswordAuthPage(self._session, self.html)
        page.input_credit_charge_password(password)
        self.html = page.click_next()

    def charge(self, value: int):
        page = CreditChargeMenuPage(self._session, self.html)
        self.html = page.click_charge()

        page = CreditChargeInputPage(self._session, self.html)
        page.input_charge_amount(value)
        self.html = page.click_next()

        page = CreditChargeConfirmPage(self._session, self.html)
        self.html = page.click_confirm()

    def cancel(self, password):
        page = CreditChargeMenuPage(self._session, self.html)
        self.html = page.click_cancel()

        page = CreditChargeCancelPage(self._session, self.html)
        page.input_credit_charge_password(password)
        self.html = page.click_next()

        page = CreditChargeCancelConfirmPage(self._session, self.html)
        self.html = page.click_confirm()

    def register_giftcode(self, code):
        page = MenuPage(self._session, self.html)
        self.html = page.click_register_gift()

        page = RegisterGiftPage(self._session, self.html)
        self.html = page.click_accept()

        page = RegisterGiftCodeInputPage(self._session, self.html)
        page.input_code(code)
        self.html = page.click_submit()

        page = RegisterGiftCodeConfirmPage(self._session, self.html)
        self.html = page.click_confirm()

