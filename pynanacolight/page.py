# -*- coding: utf-8 -*-
from requests import session
from pynanacolight.parser import *


class BasePage:
    _url = 'https://www.nanaco-net.jp/pc/emServlet'
    parser = None
    session = None

    ENCODING = 'Shift_jis'

    def __init__(self):
        BasePage.session = session()
        self.url_menu = ''
        self.url_credit_charge_menu = ''
        self.url_credit_charge = ''
        self.url_credit_charge_history = ''
        self.url_credit_charge_cancel = ''
        self.can_credit_charge = False

    @property
    def url(self):
        return self._url


class LoginPage(BasePage):
    def __init__(self):
        super().__init__()
        html = BasePage.session.get(self.url)
        html.encoding = BasePage.ENCODING

        self.parser = LoginPageParser()
        self.parser.feed(html.text)

    def input_nanaco_number(self, nanaco_number):
        self.parser.input_nanaco_number(nanaco_number)

    def input_card_number(self, card_number):
        self.parser.input_card_number(card_number)

    def click_login(self):
        self.parser.click_login()

        payload = self.parser.payload

        html = self.session.post(self.url, payload)
        html.encoding = BasePage.ENCODING

        parser = MenuPageParser()
        parser.feed(html.text)

        BasePage.url_menu = parser.url_menu.replace('emServlet', self._url)
        BasePage.url_credit_charge_menu = parser.url_credit_charge_menu.replace('emServlet', self._url)

        return MenuPage()


class MenuPage(BasePage):
    def __init__(self):
        url = BasePage.url_menu

        html = BasePage.session.get(url)
        html.encoding = BasePage.ENCODING

        self.parser = MenuPageParser()
        self.parser.feed(html.text)

        self._balance_card = self.parser.balance_card
        self._balnace_center = self.parser.balance_center

    def login_credit_charge(self, password):
        url = BasePage.url_credit_charge_menu

        html = BasePage.session.get(url)
        html.encoding = BasePage.ENCODING

        self.parser = CCPasswordAuthPageParser()
        self.parser.feed(html.text)

        # ページ入力操作
        self.parser.input_credit_charge_password(password)
        self.parser.click_next()

        payload = self.parser.payload

        html = self.session.post(self.url, payload)
        html.encoding = BasePage.ENCODING

        self.parser = CCMenuPageParser()
        self.parser.feed(html.text)

        try:
            BasePage.url_credit_charge = self.parser._credit_charge_do_url.replace('emServlet', self._url)
            BasePage.url_credit_charge_cancel = self.parser._credit_charge_cancel_url.replace('emServlet', self._url)
            BasePage.url_credit_charge_history = self.parser._credit_charge_history_url.replace('emServlet', self._url)

            BasePage.can_credit_charge = True
            return CCMenuPage()

        except AttributeError:
            return MenuPage()

    @property
    def balance_card(self):
        return self._balance_card

    @property
    def balance_center(self):
        return self._balnace_center


class CCHistoryPage(BasePage):
    def __init__(self):
        url = BasePage.url_credit_charge_history

        html = BasePage.session.get(url)
        html.encoding = BasePage.ENCODING

        self.parser = CCHistoryPageParser()
        self.parser.feed(html.text)

        self._registered_credit_card = self.parser.registered_credit_card
        self._charge_count = self.parser.charge_count
        self._charge_amount = self.parser.charge_amount

    @property
    def registered_credit_card(self):
        return self._registered_credit_card if self._registered_credit_card else ''

    @property
    def charge_count(self):
        return self._charge_count

    @property
    def charge_amount(self):
        return self._charge_amount


class CCMenuPage(BasePage):
    def __init__(self):
        url = BasePage.url_credit_charge_menu

        html = BasePage.session.get(url)
        html.encoding = BasePage.ENCODING

        self.parser = CCMenuPageParser()
        self.parser.feed(html.text)

    def charge(self, amount):
        url = BasePage.url_credit_charge

        html = BasePage.session.get(url)
        html.encoding = BasePage.ENCODING

        self.parser = CCInputPageParser()
        self.parser.feed(html.text)

        # ページ入力操作
        self.parser.input_charge_amount(amount)
        self.parser.click_next()

        payload = self.parser.payload

        html = self.session.post(self.url, payload)
        html.encoding = BasePage.ENCODING

        self.parser = CCConfirmPageParser()
        self.parser.feed(html.text)

        # ページ入力操作
        self.parser.click_confirm()

        payload = self.parser.payload
        self.session.post(self.url, payload)

    def release(self, password):
        html = self.session.get(self.url_credit_charge_cancel)

        self.parser = CCCancelPageParser()
        self.parser.feed(html.text)

        # ページ入力操作
        self.parser.input_credit_charge_password(password)
        self.parser.click_next()

        payload = self.parser.payload
        html = self.session.post(self.url, payload)

        self.parser = CCCancelConfirmPageParser()
        self.parser.feed(html.text)

        # ページ入力操作
        self.parser.click_confirm()

        payload = self.parser.payload
        self.session.post(self.url, payload)
