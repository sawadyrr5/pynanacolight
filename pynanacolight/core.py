# -*- coding: utf-8 -*-
from pynanacolight.page import *

import logging
from logging import getLogger, StreamHandler, Formatter

logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.DEBUG)

handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)

logger.addHandler(stream_handler)


class Nanaco:
    def __init__(self):
        self._balance_card = None
        self._balance_center = None

        self._charge_count = None
        self._charge_amount = None
        self._registerd_credit_card = None

        self.page = None

    def login(self, nanaco_number, card_number):
        # self.nanaco_number = nanaco_number
        # self.card_number = card_number

        self.page = LoginPage()
        self.page.input_nanaco_number(nanaco_number)
        self.page.input_card_number(card_number)
        self.page = self.page.click_login()

        logger.info("login: " + nanaco_number + " " + card_number)

        self._balance_card = self.page.balance_card
        self._balance_center = self.page.balance_center

        logger.info("balance_card: " + self.balance_card)
        logger.info("balance_center: " + self.balance_center)

    def login_credit_charge(self, password):
        self.page = MenuPage()
        self.page = self.page.login_credit_charge(password)

        if isinstance(self.page, CCMenuPage):
            logger.info("login credit charge succeed")

            self.page = CCHistoryPage()

            self._registerd_credit_card = self.page.registered_credit_card
            self._charge_amount = self.page.charge_amount
            self._charge_count = self.page.charge_count

            logger.info("registered credit card: " + self._registerd_credit_card if self._registerd_credit_card else '')
            logger.info("charge count: " + self.charge_count if self.charge_count else '')
            logger.info("charge amount: " + self.charge_amount if self.charge_amount else '')
        else:

            logger.info("login credit charge failed")

    def charge(self, amount):
        self.page = CCMenuPage()
        self.page.charge(amount)

    def release(self, password):
        self.page = CCMenuPage()
        self.page.release(password)

    @property
    def balance_card(self):
        return self._balance_card

    @property
    def balance_center(self):
        return self._balance_center

    @property
    def registered_credit_card(self):
        return self._registerd_credit_card

    @property
    def charge_count(self):
        return self._charge_count

    @property
    def charge_amount(self):
        return self._charge_amount
