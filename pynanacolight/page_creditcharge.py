# -*- coding: utf-8 -*-
"""
ページの抽象レベル操作を行う
"""
from requests import session
from urllib.parse import urlencode

from pynanacolight.page import ENCODING, BASE_URL, DEFAULT_INPUT_DATA, logger
from pynanacolight.parser import InputTagParser,AnchorTagParser,CreditChargeHistoryParser


class CreditChargePasswordAuthPage:

    def __init__(self, session: session(), html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        names = DEFAULT_INPUT_DATA
        names.append("_WBSessionID")

        self.data = {k: v for k, v in parser.data.items() if k in names}

    def input_credit_charge_password(self, password):
        data = {
            "CRDT_CHEG_PWD": password
        }
        self.data.update(data)

        logger.info("input_credit_charge_password: " + str(data))

    def click_next(self):
        data = {
            "ACT_ACBS_do_CRDT_CHRG_PWD_AUTH": '次へ'
        }
        self.data.update(data)

        url = BASE_URL
        data = self.data

        logger.info("click_next: " + str(url))

        html = self._session.post(url, data)
        html.encoding = ENCODING

        return html


class CreditChargeMenuPage:
    _DATA_CHARGE = {
        "_ActionID": 'ACBS_do_CRDT_CHRG',
        "_ControlID": 'BS_PCB8001_Control',
        "_PageID": 'SCBS_PCB8001'
    }

    _DATA_HISTORY = {
        "_ActionID": 'ACBS_do_CRDT_TRADE_HISTORY_CONF',
        "_ControlID": 'BS_PCB8001_Control',
        "_PageID": 'SCBS_PCB8001'
    }

    _DATA_CANCEL = {
        "_ActionID": 'ACBS_do_CRDT_CNCL',
        "_ControlID": 'BS_PCB8001_Control',
        "_PageID": 'SCBS_PCB8001'
    }

    def __init__(self, session: session(), html):
        self._session = session
        self._html = html

        parser = AnchorTagParser()
        parser.feed(html.text)

        # prepare parameter
        self.data = {}
        self.data.update({"_SeqNo": parser.anchors[0]['_SeqNo'][0]})
        self.data.update({"_WBSessionID": parser.anchors[0]['_WBSessionID'][0]})
        self.data.update({"_DataStoreID": parser.anchors[0]['_DataStoreID'][0]})

    def click_charge(self):
        data = self.__class__._DATA_CHARGE
        self.data.update(data)

        qs = urlencode(self.data)
        url = BASE_URL + '?' + qs

        logger.info("click_charge: " + str(url))

        html = self._session.get(url)
        html.encoding = ENCODING

        return html

    def click_history(self):
        data = self.__class__._DATA_HISTORY
        self.data.update(data)

        qs = urlencode(self.data)
        url = BASE_URL + '?' + qs

        logger.info("click_history: " + str(url))

        html = self._session.get(url)
        html.encoding = ENCODING

        return html

    def click_cancel(self):
        data = self.__class__._DATA_CANCEL
        self.data.update(data)

        qs = urlencode(self.data)
        url = BASE_URL + '?' + qs

        logger.info("click_cancel: " + str(url))

        html = self._session.get(url)
        html.encoding = ENCODING

        return html


class CreditChargeHistoryPage:

    def __init__(self, session: session(), html):
        self._session = session

        self._registered_credit_card = ''
        self._charge_count = None
        self._charge_amount = None

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

    def __init__(self, session: session(), html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        names = DEFAULT_INPUT_DATA
        names.append("_WBSessionID")

        self.data = {k: v for k, v in parser.data.items() if k in names}

    def input_charge_amount(self, amount):
        data = {
            "AMT": amount
        }
        self.data.update(data)

        logger.info("input_charge_amount: " + str(data))

    def click_next(self):
        data = {
            "ACT_ACBS_do_CRDT_CHRG_INPUT": '次へ'
        }
        self.data.update(data)

        url = BASE_URL
        data = self.data

        logger.info("click_next: " + str(data))

        html = self._session.post(url, data)
        html.encoding = ENCODING

        return html


class CreditChargeConfirmPage:
    def __init__(self, session: session(), html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        names = DEFAULT_INPUT_DATA
        names.append("_WBSessionID")
        names.append("SESSION_ID")

        self.data = {k: v for k, v in parser.data.items() if k in names}

    def click_confirm(self):
        data = {
            "ACT_ACBS_do_CRDT_CHRG_CONF": '申込み'
        }
        self.data.update(data)

        url = BASE_URL
        data = self.data

        logger.info("click confirm: " + str(data))

        html = self._session.post(url, data)
        html.encoding = ENCODING

        return html


class CreditChargeCancelPage:
    def __init__(self, session: session(), html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        names = DEFAULT_INPUT_DATA
        names.append("_WBSessionID")

        self.data = {k: v for k, v in parser.data.items() if k in names}

    def input_credit_charge_password(self, password):
        data = {
            "CRDT_CHEG_PWD": password
        }
        self.data.update(data)

        logger.info("input_credit_charge_password: " + str(data))

    def click_next(self):
        data = {
            "ACT_ACBS_do_CRDT_CNCL_INPUT": '解約確認画面へ'
        }
        self.data.update(data)

        url = BASE_URL
        data = self.data

        logger.info("click_next: " + str(data))

        html = self._session.post(url, data)
        html.encoding = ENCODING

        return html


class CreditChargeCancelConfirmPage:
    def __init__(self, session: session(), html):
        self._session = session
        self._html = html

        parser = InputTagParser()
        parser.feed(html.text)

        names = DEFAULT_INPUT_DATA
        names.append("_WBSessionID")

        self.data = {k: v for k, v in parser.data.items() if k in names}

    def click_confirm(self):
        data = {
            "ACT_ACBS_do_CRDT_CNCL_CONF": ''
        }
        self.data.update(data)

        url = BASE_URL
        data = self.data

        logger.info("click_confirm: " + str(data))

        html = self._session.post(url, data)
        html.encoding = ENCODING

        return html