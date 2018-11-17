# -*- coding: utf-8 -*-
"""
ページの要素レベル操作を行う
"""
from html.parser import HTMLParser
from urllib.parse import parse_qs
from datetime import datetime as dt


# Internal -- 全てのINPUTタグをパースしてdictを返す
class InputTagParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.data = {}

    def handle_starttag(self, tag, attrs):

        if tag == 'input':
            dict_attrs = dict(attrs)

            if dict_attrs.keys() >= {'name', 'value'}:
                item = {dict_attrs['name']: dict_attrs['value']}

                self.data.update(item)

    def error(self, message):
        pass


# Internal -- すべてのAタグをパースしてhref属性のリストを返す
class AnchorTagParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.anchors = []

    def handle_starttag(self, tag, attrs):

        if tag == 'a':
            dict_attrs = dict(attrs)

            if 'href' in dict_attrs.keys():
                qs = dict_attrs['href']
                qs = qs.replace('emServlet?', '')

                if '_ActionID' in qs:
                    self.anchors.append(parse_qs(qs))

    def error(self, message):
        pass


# Internal -- メニューページのPタグをパースする
class BalanceParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self._amount = []
        self._timestamp = []

        self.balance_card = None
        self.balance_center = None
        self.balance_card_timestamp = None
        self.balance_center_timestamp = None

    def handle_data(self, data):
        if self.lasttag == 'p' and '円' in data:
            data = data.replace('円', '').replace(',', '')
            self._amount.append(data)

            if len(self._amount) == 2:
                self.balance_card = int(self._amount[0])
                self.balance_center = int(self._amount[1])

        if self.lasttag == 'span' and '時点' in data:
            data = data.replace('時点', '')
            self._timestamp.append(dt.strptime(data, "%Y年%m月%d日%H時%M分"))

            if len(self._timestamp) == 2:
                self.balance_card_timestamp = self._timestamp[0]
                self.balance_center_timestamp = self._timestamp[1]

    def error(self, message):
        pass


# Internal -- クレジットチャージ履歴ページをパースする
class CreditChargeHistoryParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.registered_credit_card = None
        self._charge_count = []
        self.charge_count = None
        self._charge_amount = []
        self.charge_amount = None

    def handle_data(self, data):
        if self.lasttag == 'p' and '登録クレジットカード：' in data:
            data = data.replace('登録クレジットカード：', '')
            self.registered_credit_card = data

        if self.lasttag == 'td' and '回' in data:
            data = data.replace('回', '')
            self._charge_count.append(data)

            if len(self._charge_count) > 1:
                self.charge_count = int(self._charge_count[1])

        if self.lasttag == 'td' and '円' in data:
            data = data.replace('円', '').replace(',', '')
            self._charge_amount.append(data)

            if len(self._charge_amount) > 1:
                self.charge_amount = int(self._charge_amount[1])

    def error(self, message):
        pass


# Internal -- タイトルタグをパースする
class TitleParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.title = ''

    def handle_data(self, data):
        if self.lasttag == 'title' and self.title == '':
            self.title = data

    def error(self, message):
        pass


# Internal -- ギフト額面などをパースする
class GiftAmountParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.gift_has_registered = False
        self.gift_amount = None
        self.gift_receivable_date = None

    def handle_data(self, data):
        if self.lasttag == 'strong' and u'このギフトIDは、すでに下記の通り登録済です。' in data:
            self.gift_has_registered = True

        if self.lasttag == 'td' and '円' in data:
            self.gift_amount = data.replace('円', '')

        if self.lasttag == 'td' and 'から' in data:
            data = data.replace('から', '')
            self.gift_receivable_date = dt.strptime(data, "%Y/%m/%d %p%I:00")

    def error(self, message):
        pass


# Internal -- ギフト登録結果をパースする
class RegisterGiftCodeResultPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.gift_receivable_date = None

    def handle_data(self, data):
        if self.lasttag == 'td' and 'から' in data:
            data = data.replace('から', '')
            self.gift_receivable_date = dt.strptime(data, "%Y/%m/%d %p%I:00")

    def error(self, message):
        pass
