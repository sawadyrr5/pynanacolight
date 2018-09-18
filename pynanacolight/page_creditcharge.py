# -*- coding: utf-8 -*-
"""
ページの抽象レベル操作を行う
"""
from requests import session

from pynanacolight.page import BASE_URL, DEFAULT_INPUT_DATA_NAMES, _get, _post
from pynanacolight.parser import InputTagParser, AnchorTagParser, CreditChargeHistoryParser
from pynanacolight.util.logger import logging


class CreditChargePasswordAuthPage:

    def __init__(self, session: session(), html):
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

        html = _post(
            session=self._session,
            url=BASE_URL,
            data=self.data
        )
        return html


class CreditChargeMenuPage:

    def __init__(self, session: session(), html):
        self._session = session

        parser = AnchorTagParser()
        parser.feed(html.text)

        # prepare parameter
        self.data = {}
        self.data.update({"_SeqNo": parser.anchors[0]['_SeqNo'][0]})
        self.data.update({"_WBSessionID": parser.anchors[0]['_WBSessionID'][0]})
        self.data.update({"_DataStoreID": parser.anchors[0]['_DataStoreID'][0]})

    @logging
    def click_charge(self):
        self.data.update(
            {
                "_ActionID": 'ACBS_do_CRDT_CHRG',
                "_ControlID": 'BS_PCB8001_Control',
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
    def click_history(self):
        self.data.update(
            {
                "_ActionID": 'ACBS_do_CRDT_TRADE_HISTORY_CONF',
                "_ControlID": 'BS_PCB8001_Control',
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
    def click_cancel(self):
        self.data.update(
            {
                "_ActionID": 'ACBS_do_CRDT_CNCL',
                "_ControlID": 'BS_PCB8001_Control',
                "_PageID": 'SCBS_PCB8001'
            }
        )

        html = _get(
            session=self._session,
            url=BASE_URL,
            param=self.data
        )
        return html


class CreditChargeHistoryPage:

    def __init__(self, session: session(), html):
        self._session = session

        self._registered_credit_card = ''
        self._charge_count = None
        self._charge_amount = None

        # read credit charge information.
        parser = CreditChargeHistoryParser()
        parser.feed(html.text)

        self._registered_credit_card = parser.registered_credit_card
        self._charge_count = parser.charge_count
        self._charge_amount = parser.charge_amount[0]

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

    def __init__(self, session: session(), html):
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

        html = _post(
            session=self._session,
            url=BASE_URL,
            data=self.data
        )
        return html


class CreditChargeConfirmPage:
    def __init__(self, session: session(), html):
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

        html = _post(
            session=self._session,
            url=BASE_URL,
            data=self.data
        )
        return html


class CreditChargeCancelPage:
    def __init__(self, session: session(), html):
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

        html = _post(
            session=self._session,
            url=BASE_URL,
            data=self.data
        )
        return html


class CreditChargeCancelConfirmPage:
    def __init__(self, session: session(), html):
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

        html = _post(
            session=self._session,
            url=BASE_URL,
            data=self.data
        )
        return html
