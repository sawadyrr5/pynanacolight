# -*- coding: utf-8 -*-
"""
ページの抽象レベル操作を行う
"""
from requests import Session

from pynanacolight.page import BASE_URL, ENCODING, DEFAULT_INPUT_DATA_NAMES
from pynanacolight.parser import InputTagParser, AnchorTagParser, \
    CreditChargeHistoryParser
from pynanacolight.util import logging


class CreditChargePasswordAuthPage:

    def __init__(self, session: Session, html):
        self._session = session

        parser = InputTagParser()
        parser.feed(html.text)

        wanted_keys = DEFAULT_INPUT_DATA_NAMES + ["_WBSessionID"]
        self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}

    @logging
    def input_credit_charge_password(self, password):
        self.data.update(
            {
                "CRDT_CHEG_PWD": password
            }
        )

    @logging
    def click_next(self):
        self.data.update(
            {
                "ACT_ACBS_do_CRDT_CHRG_PWD_AUTH": '次へ'
            }
        )

        html = self._session.post(BASE_URL, self.data)
        html.encoding = ENCODING
        return html


# class CreditChargeRegisterGuidePage:
#
#     def __init__(self, session: Session, html):
#         self._session = session
#
#         parser = InputTagParser()
#         parser.feed(html.text)
#
#         wanted_keys = DEFAULT_INPUT_DATA_NAMES + ["_WBSessionID"]
#         self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}
#
#     @logging
#     def click_next(self):
#         self.data.update(
#             {
#                 "ACT_ACBS_do_CRDT_REG_GUIDE_NEXT": '次へ'
#             }
#         )
#
#         html = _post(
#             session=self._session,
#             url=BASE_URL,
#             data=self.data
#         )
#         return html
#
#
# class CreditChargeRegisterAgreePage:
#
#     def __init__(self, session: Session, html):
#         self._session = session
#
#         parser = InputTagParser()
#         parser.feed(html.text)
#
#         wanted_keys = DEFAULT_INPUT_DATA_NAMES + ["_WBSessionID"]
#         self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}
#
#     @logging
#     def click_agree(self):
#         self.data.update(
#             {
#                 "ACT_ACBS_do_CRDT_REG_AGREE": '特約に同意の上、登録'
#             }
#         )
#
#         html = _post(
#             session=self._session,
#             url=BASE_URL,
#             data=self.data
#         )
#         return html
#
#
# class CreditChargeRegisterInputPage1:
#
#     def __init__(self, session: Session, html):
#         self._session = session
#
#         parser = InputTagParser()
#         parser.feed(html.text)
#
#         wanted_keys = DEFAULT_INPUT_DATA_NAMES + ["_WBSessionID"]
#         self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}
#
#     @logging
#     def input_creditcard_number_1(self, number):
#         self.data.update(
#             {
#                 "CRDT_CARD_NO_1": number
#             }
#         )
#
#     @logging
#     def input_creditcard_number_2(self, number):
#         self.data.update(
#             {
#                 "CRDT_CARD_NO_2": number
#             }
#         )
#
#     @logging
#     def input_creditcard_number_3(self, number):
#         self.data.update(
#             {
#                 "CRDT_CARD_NO_3": number
#             }
#         )
#
#     @logging
#     def input_creditcard_number_4(self, number):
#         self.data.update(
#             {
#                 "CRDT_CARD_NO_4": number
#             }
#         )
#
#     @logging
#     def input_creditcard_expire_month(self, month):
#         self.data.update(
#             {
#                 "CRDT_CARD_VALID_LMT_MONTH": month
#             }
#         )
#
#     @logging
#     def input_creditcard_expire_year(self, year):
#         self.data.update(
#             {
#                 "CRDT_CARD_VALID_LMT_YEAR": year
#             }
#         )
#
#     @logging
#     def input_security_code(self, code):
#         self.data.update(
#             {
#                 "CRDT_SECURITY_CD": code
#             }
#         )
#
#     @logging
#     def input_phone_number(self, phone_number):
#         self.data.update(
#             {
#                 "DEC_TEL_NO": phone_number
#             }
#         )
#
#     @logging
#     def click_next(self):
#         self.data.update(
#             {
#                 "ACT_ACBS_do_CRDT_REG_INPUT1": '次へ'
#             }
#         )
#
#         html = _post(
#             session=self._session,
#             url=BASE_URL,
#             data=self.data
#         )
#         return html
#
#
# class CreditChargeRegisterInputPage2:
#
#     def __init__(self, session: Session, html):
#         self._session = session
#
#         parser = InputTagParser()
#         parser.feed(html.text)
#
#         wanted_keys = DEFAULT_INPUT_DATA_NAMES + ["_WBSessionID"]
#         self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}
#
#     @logging
#     def input_kana_name(self, name):
#         self.data.update(
#             {
#                 "NAME_KN": name.encode(ENCODING)
#             }
#         )
#
#     @logging
#     def input_birth_year(self, year):
#         self.data.update(
#             {
#                 "BTHD_YEAR": year
#             }
#         )
#
#     @logging
#     def input_birth_month(self, month):
#         self.data.update(
#             {
#                 "BTHD_MONTH": month
#             }
#         )
#
#     @logging
#     def input_birth_day(self, day):
#         self.data.update(
#             {
#                 "BTHD_DAY": day
#             }
#         )
#
#     @logging
#     def input_creditcharge_password(self, password):
#         self.data.update(
#             {
#                 "CRDT_CHEG_PWD": password,
#                 "CRDT_CHEG_PWD_CONF": password
#             }
#         )
#
#     @logging
#     def input_email(self, email):
#         self.data.update(
#             {
#                 "REG_EMAIL": email,
#                 "REG_EMAIL_CONF": email
#             }
#         )
#
#     @logging
#     def select_send_information(self, send=False):
#         self.data.update(
#             {
#                 "VAL_INF_SND_FLG": 1 if send else 2
#             }
#         )
#
#     @logging
#     def click_next(self):
#         self.data.update(
#             {
#                 "ACT_ACBS_do_CRDT_REG_INPUT2": '次へ'
#             }
#         )
#
#         html = _post(
#             session=self._session,
#             url=BASE_URL,
#             data=self.data
#         )
#         return html
#
#
# class CreditChargeRegisterConfirmPage:
#
#     def __init__(self, session: Session, html):
#         self._session = session
#
#         parser = InputTagParser()
#         parser.feed(html.text)
#
#         wanted_keys = DEFAULT_INPUT_DATA_NAMES + ["_WBSessionID"]
#         self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}
#
#     @logging
#     def click_confirm(self):
#         self.data.update(
#             {
#                 "ACT_ACBS_do_CRDT_REG_CONF": '登録する'
#             }
#         )
#
#         html = _post(
#             session=self._session,
#             url=BASE_URL,
#             data=self.data
#         )
#         return html


class CreditChargeMenuPage:
    """creadit charge menu page

    Returns:
        _type_: _description_
    """

    @logging
    def __init__(self, session: Session, html):
        self._session = session

        parser = AnchorTagParser()
        parser.feed(html.text)

        # prepare parameter
        self.data = {}
        self.data.update({"_SeqNo": parser.anchors[0]['_SeqNo'][0]})
        self.data.update(
            {"_WBSessionID": parser.anchors[0]['_WBSessionID'][0]})
        self.data.update(
            {"_DataStoreID": parser.anchors[0]['_DataStoreID'][0]})

    @logging
    def click_charge(self):
        self.data.update(
            {
                "_ActionID": 'ACBS_do_CRDT_CHRG',
                "_ControlID": 'BS_PCB8001_Control',
                "_PageID": 'SCBS_PCB8001'
            }
        )
        html = self._session.get(BASE_URL, self.data)
        html.encoding = ENCODING
        return html

    @logging
    def click_history(self):
        self.data.update(
            {
                "_ActionID": 'ACBS_do_CRDT_TRADE_HISTORY_CONF',
                "_ControlID": 'BS_PCB8001_Control',
                "_PageID": 'SCBS_PCB8001'
            }
        )
        html = self._session.get(BASE_URL, self.data)
        html.encoding = ENCODING
        return html

    @logging
    def click_cancel(self):
        self.data.update(
            {
                "_ActionID": 'ACBS_do_CRDT_CNCL',
                "_ControlID": 'BS_PCB8001_Control',
                "_PageID": 'SCBS_PCB8001'
            }
        )
        html = self._session.get(BASE_URL, self.data)
        html.encoding = ENCODING
        return html


class CreditChargeHistoryPage:
    """credit charge history page
    """

    def __init__(self, session: Session, html):
        self._session = session

        self._registered_credit_card = ''
        self._charge_count = None
        self._charge_amount = None

        # read credit charge information.
        parser = CreditChargeHistoryParser()
        parser.feed(html.text)

        self._registered_credit_card = parser.registered_credit_card
        self._charge_count = parser.charge_count
        self._charge_amount = parser.charge_amount

    @property
    def text_registered_credit_card(self):
        return self._registered_credit_card

    @property
    def text_charge_count(self):
        return self._charge_count

    @property
    def text_charge_amount(self):
        return self._charge_amount


class CreditChargeInputPage:
    """credit charge input page
    """

    def __init__(self, session: Session, html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        wanted_keys = DEFAULT_INPUT_DATA_NAMES + ["_WBSessionID"]
        self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}

    @logging
    def input_charge_amount(self, amount):
        self.data.update(
            {
                "AMT": amount
            }
        )

    @logging
    def click_next(self):
        self.data.update(
            {
                "ACT_ACBS_do_CRDT_CHRG_INPUT": '次へ'
            }
        )

        html = self._session.post(BASE_URL, self.data)
        html.encoding = ENCODING
        return html


class CreditChargeConfirmPage:
    def __init__(self, session: Session, html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        wanted_keys = DEFAULT_INPUT_DATA_NAMES + ["_WBSessionID", "SESSION_ID"]
        self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}

    @logging
    def click_confirm(self):
        self.data.update(
            {
                "ACT_ACBS_do_CRDT_CHRG_CONF": '申込み'
            }
        )

        html = self._session.post(BASE_URL, self.data)
        html.encoding = ENCODING
        return html


class CreditChargeCancelPage:
    def __init__(self, session: Session, html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        wanted_keys = DEFAULT_INPUT_DATA_NAMES + ["_WBSessionID"]
        self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}

    @logging
    def input_credit_charge_password(self, password):
        self.data.update(
            {
                "CRDT_CHEG_PWD": password
            }
        )

    @logging
    def click_next(self):
        self.data.update(
            {
                "ACT_ACBS_do_CRDT_CNCL_INPUT": '解約確認画面へ'
            }
        )

        html = self._session.post(BASE_URL, self.data)
        html.encoding = ENCODING
        return html


class CreditChargeCancelConfirmPage:
    def __init__(self, session: Session, html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        wanted_keys = DEFAULT_INPUT_DATA_NAMES + ["_WBSessionID"]
        self.data = {k: v for k, v in parser.data.items() if k in wanted_keys}

    @logging
    def click_confirm(self):
        self.data.update(
            {
                "ACT_ACBS_do_CRDT_CNCL_CONF": ''
            }
        )

        html = self._session.post(BASE_URL, self.data)
        html.encoding = ENCODING
        return html
