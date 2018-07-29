# -*- coding: utf-8 -*-
from html.parser import HTMLParser


class BasePageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._payload = {}
        self._payload_keys = [
            "_PageID",
            "_DataStoreID",
            "_SeqNo",
            "_ControlID",
            "_WID",
            "_ORGWID",
            "_WIDManager",
            "_preProcess",
            "_TimeOutControl",
            "_WIDMode",
            "_WindowName",
            "_ReturnPageInfo"
        ]

    def feed(self, data):
        super().feed(data)

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            tmp = dict(attrs)
            if tmp['name'] in self._payload_keys:
                self._payload.update(
                    {
                        tmp['name']: tmp['value']
                    }
                )

    @property
    def payload(self):
        return self._payload


class LoginPageParser(BasePageParser):
    def input_nanaco_number(self, nanaco_number):
        self._payload["XCID"] = nanaco_number

    def input_card_number(self, card_number):
        self._payload["SECURITY_CD"] = card_number

    def click_login(self):
        self._payload["ACT_ACBS_do_LOGIN2"] = ''

    @property
    def payload(self):
        return super().payload


class MenuPageParser(BasePageParser):
    def __init__(self):
        super().__init__()
        self._charge_amount = []
        self.url_menu = ''
        self.url_credit_charge_menu = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and '_ActionID=ACBS_do_MEMBER_MENU' in attr[1]:
                    self.url_menu = attr[1]

                if attr[0] == 'href' and '_ActionID=ACBS_do_CRDT_TRADE_MENU' in attr[1]:
                    self.url_credit_charge_menu = attr[1]

    def handle_data(self, data):
        if self.lasttag == 'p' and '円' in data:
            self._charge_amount.append(data)

    @property
    def payload(self):
        # self._payload = super().payload
        # return self._payload
        return super().payload

    @property
    def balance_card(self):
        return self._charge_amount[0].replace('円', '').replace(',', '')

    @property
    def balance_center(self):
        return self._charge_amount[1].replace('円', '').replace(',', '')


class CCPasswordAuthPageParser(BasePageParser):
    def input_credit_charge_password(self, password):
        self._payload["CRDT_CHEG_PWD"] = password

    def click_next(self):
        self._payload["ACT_ACBS_do_CRDT_CHRG_PWD_AUTH"] = '次へ'

    @property
    def payload(self):
        return super().payload


class CCMenuPageParser(BasePageParser):
    def __init__(self):
        super().__init__()
        self._credit_charge_menu_url = None
        self._credit_charge_do_url = None
        self._credit_charge_history_url = None
        self._credit_charge_cancel_url = None

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and '_ActionID=ACBS_do_CRDT_CHRG' in attr[1]:
                    self._credit_charge_do_url = attr[1]
                elif attr[0] == 'href' and '_ActionID=ACBS_do_CRDT_TRADE_HISTORY_CONF' in attr[1]:
                    self._credit_charge_history_url = attr[1]
                elif attr[0] == 'href' and '_ActionID=ACBS_do_CRDT_CNCL' in attr[1]:
                    self._credit_charge_cancel_url = attr[1]

    @property
    def credit_charge_do_url(self):
        return self._credit_charge_do_url

    @property
    def credit_charge_history_url(self):
        return self._credit_charge_history_url

    @property
    def credit_charge_cancel_url(self):
        return self._credit_charge_cancel_url

    @property
    def payload(self):
        return super().payload


class CCHistoryPageParser(BasePageParser):
    def __init__(self):
        super().__init__()
        self._credit_charge_menu_url = None
        self._registered_credit_card = None
        self._charge_count = None
        self._charge_amount = []

    def handle_data(self, data):
        if self.lasttag == 'p' and '登録クレジットカード：' in data:
            self._registered_credit_card = data

        if self.lasttag == 'td' and '回' in data:
            self._charge_count = data

        if self.lasttag == 'td' and '円' in data:
            self._charge_amount.append(data)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and '_ActionID=ACBS_do_CRDT_TRADE_MENU' in attr[1]:
                    self._credit_charge_menu_url = attr[1]

    @property
    def credit_charge_menu_url(self):
        return self._credit_charge_menu_url

    @property
    def registered_credit_card(self):
        return self._registered_credit_card.replace('登録クレジットカード：', '')

    @property
    def charge_count(self):
        return self._charge_count.replace('回', '')

    @property
    def charge_amount(self):
        return self._charge_amount[1].replace('円', '').replace(',', '') if self._charge_amount else None


class CCInputPageParser(BasePageParser):
    def __init__(self):
        super().__init__()
        self._payload = super().payload
        self._payload_keys.append("_WBSessionID")

    def input_charge_amount(self, amount):
        self._payload["AMT"] = amount

    def click_next(self):
        self._payload["ACT_ACBS_do_CRDT_CHRG_INPUT"] = '次へ'

    @property
    def payload(self):
        return super().payload


class CCConfirmPageParser(BasePageParser):
    def __init__(self):
        super().__init__()
        self._payload = super().payload
        self._payload_keys.append("_WBSessionID")
        self._payload_keys.append("SESSION_ID")

    def click_confirm(self):
        self._payload["ACT_ACBS_do_CRDT_CHRG_CONF"] = '申込み'

    @property
    def payload(self):
        # self._payload = super().payload
        # return self._payload
        return super().payload


class CCCancelPageParser(BasePageParser):
    def __init__(self):
        super().__init__()
        self._payload = super().payload
        self._payload_keys.append("_WBSessionID")

    def input_credit_charge_password(self, password):
        self._payload["CRDT_CHEG_PWD"] = password

    def click_next(self):
        self._payload["ACT_ACBS_do_CRDT_CNCL_INPUT"] = '解約確認画面へ'

    @property
    def payload(self):
        return super().payload


class CCCancelConfirmPageParser(BasePageParser):
    def __init__(self):
        super().__init__()
        self._payload = super().payload
        self._payload_keys.append("_WBSessionID")

    def input_credit_charge_password(self, password):
        self._payload["CRDT_CHEG_PWD"] = password

    def click_confirm(self):
        self._payload["ACT_ACBS_do_CRDT_CNCL_CONF"] = ''

    @property
    def payload(self):
        return super().payload
