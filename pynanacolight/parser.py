# -*- coding: utf-8 -*-
"""
ページの要素レベル操作を行う
"""
from html.parser import HTMLParser
from urllib.parse import parse_qs


# Internal -- parse all <INPUT> tags, and return dictionary object.
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


# Internal -- parse all <A> tags, and return list of href attribute.
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


# Internal -- parse menu page <P> tags.
class BalanceParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.amount = []

    def handle_data(self, data):
        if self.lasttag == 'p' and '円' in data:
            data = data.replace('円', '').replace(',', '')
            self.amount.append(data)

    def error(self, message):
        pass


# Internal -- parse credit charge history page tags.
class CreditChargeHistoryParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.registered_credit_card = ''
        self.charge_count = ''
        self.charge_amount = []

    def handle_data(self, data):
        if self.lasttag == 'p' and '登録クレジットカード：' in data:
            self.registered_credit_card = data

        if self.lasttag == 'td' and '回' in data:
            self.charge_count = data

        if self.lasttag == 'td' and '円' in data:
            self.charge_amount.append(data)

    def error(self, message):
        pass
