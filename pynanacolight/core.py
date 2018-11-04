# -*- coding: utf-8 -*-
from pynanacolight.page import LoginPage, MenuPage
from pynanacolight.page_creditcharge import CreditChargeMenuPage, CreditChargeHistoryPage, CreditChargePasswordAuthPage, \
    CreditChargeInputPage, CreditChargeConfirmPage, CreditChargeCancelPage, CreditChargeCancelConfirmPage
    # CreditChargeRegisterGuidePage, CreditChargeRegisterAgreePage, CreditChargeRegisterInputPage1, \
    # CreditChargeRegisterInputPage2, CreditChargeRegisterConfirmPage
from pynanacolight.page_gift import RegisterGiftPage, RegisterGiftCodeInputPage, RegisterGiftCodeConfirmPage

from requests import session


class PyNanacoLight:
    def __init__(self, _session: session()=None):
        if _session is None:
            _session = session()
        self._session = _session

        self._html = None

        self.balance_card = None
        self.balance_center = None

        self.can_credit_charge = None

        self.credit_charge_password = ''

        self.registered_creditcard = ''
        self.charge_count = None
        self.charge_amount = None

    def login(self, nanaco_number:str, card_number:str=None, password:str=None):
        page = LoginPage(self._session)

        page.input_nanaco_number(nanaco_number)

        if card_number:
            page.input_card_number(card_number)
            self._html = page.click_login_by_card_number()

        elif password:
            page.input_password(password)
            self._html = page.click_login_by_password()

        else:
            return

        page = MenuPage(self._session, self._html)
        self.balance_card = page.text_balance_card
        self.balance_center = page.text_balance_center

    def login_credit_charge(self, password:str):
        self.credit_charge_password = password

        page = MenuPage(self._session, self._html)
        self._html = page.click_login_credit_charge()

        self.can_credit_charge = page.can_credit_charge

        if self.can_credit_charge:
            page = CreditChargePasswordAuthPage(self._session, self._html)
            page.input_credit_charge_password(password)
            self._html = page.click_next()

            page = CreditChargeMenuPage(self._session, self._html)
            html = page.click_history()

            page = CreditChargeHistoryPage(self._session, html)
            self.registered_creditcard = page.text_registered_credit_card
            self.charge_count = page.text_charge_count
            self.charge_amount = page.text_charge_amount

    # def register(self,
    #              number: str,
    #              expire_month: str, expire_year: str, code: str, phone: str,
    #              name: str, birth_year: str, birth_month: str, birth_day: str, password: str, mail: str, send_info: str,
    #              security_code: str
    #              ):
    #
    #     page = MenuPage(self._session, self._html)
    #     self._html = page.click_login_credit_charge()
    #
    #     page = CreditChargeRegisterGuidePage(self._session, self._html)
    #     self._html = page.click_next()
    #
    #     page = CreditChargeRegisterAgreePage(self._session, self._html)
    #     self._html = page.click_agree()
    #
    #     page = CreditChargeRegisterInputPage1(self._session, self._html)
    #     page.input_creditcard_number_1(number[:4])
    #     page.input_creditcard_number_2(number[4:8])
    #     page.input_creditcard_number_3(number[8:12])
    #     page.input_creditcard_number_4(number[12:16])
    #
    #     page.input_creditcard_expire_month(expire_month)
    #     page.input_creditcard_expire_year(expire_year)
    #
    #     page.input_security_code(code)
    #     page.input_phone_number(phone)
    #     self._html = page.click_next()
    #
    #     page = CreditChargeRegisterInputPage2(self._session, self._html)
    #     page.input_kana_name(name)
    #     page.input_birth_year(birth_year)
    #     page.input_birth_month(birth_month)
    #     page.input_birth_day(birth_day)
    #     page.input_creditcharge_password(password)
    #     page.input_email(mail)
    #     page.select_send_information(send_info)
    #     self._html = page.click_next()
    #
    #     page = CreditChargeRegisterConfirmPage(self._session, self._html)
    #     self._html = page.click_confirm()

    def charge(self, value: int):
        page = CreditChargeMenuPage(self._session, self._html)
        self._html = page.click_charge()

        page = CreditChargeInputPage(self._session, self._html)
        page.input_charge_amount(value)
        self._html = page.click_next()

        page = CreditChargeConfirmPage(self._session, self._html)
        self._html = page.click_confirm()

    def cancel(self, password):
        page = CreditChargeMenuPage(self._session, self._html)
        self._html = page.click_cancel()

        page = CreditChargeCancelPage(self._session, self._html)
        page.input_credit_charge_password(password)
        self._html = page.click_next()

        page = CreditChargeCancelConfirmPage(self._session, self._html)
        self._html = page.click_confirm()

    def register_giftcode(self, code):
        page = MenuPage(self._session, self._html)
        self._html = page.click_register_gift()

        page = RegisterGiftPage(self._session, self._html)
        self._html = page.click_accept()

        page = RegisterGiftCodeInputPage(self._session, self._html)
        page.input_code(code)
        self._html = page.click_submit()

        page = RegisterGiftCodeConfirmPage(self._session, self._html)
        self._html = page.click_confirm()
