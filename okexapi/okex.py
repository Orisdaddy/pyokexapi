import hmac
import json
import base64
import hashlib
from urllib.parse import urlencode
from typing import Union

from .exceptions.server import ServerError
from .client import BaseExchange
from .util import *


class Okex(BaseExchange):
    v3path = '/api/{api}/{version}/{action}'
    v5path = '/api/{version}/{api}/{action}'

    def __init__(self, ak=None, secret=None, password=None, version='v5', test=False, throtable=False):
        self.ak = ak
        self.secret = secret
        self.password = password
        self.version = version
        self.test = test
        self.throtable = throtable
        self.host = 'www.okex.com'
        self.protocol = 'https'

    @staticmethod
    def sign(headers, method, path, body, secret):
        ts, now = get_date()
        headers['OK-ACCESS-TIMESTAMP'] = now
        if body is None:
            body = ''
        sts = f'{now}{method}{path}{body}'
        hash_val = hmac.new(secret.encode('utf-8'), sts.encode('utf-8'), hashlib.sha256)
        signature = base64.b64encode(hash_val.digest()).decode('utf-8')
        headers['OK-ACCESS-SIGN'] = signature
        return signature

    def parse_response(self, response):
        code = response.get('code')
        msg = response.get('msg')
        if str(code) == '0':
            return response.get('data')
        else:
            raise ServerError(200, code, msg, response)

    def prepare_sign_headers(self, method, path, body, headers):
        if self.test:
            headers['x-simulated-trading'] = '1'
        if self.ak:
            headers['OK-ACCESS-KEY'] = self.ak
        if self.secret:
            self.sign(headers, method, path, body, self.secret)
        if self.password:
            headers['OK-ACCESS-PASSPHRASE'] = self.password
        return headers

    def find_api(self, api, action, throttle=None):
        if throttle:
            self.throttle = throttle
        if self.version == 'v3':
            return self.v3path.format(version=self.version, api=api, action=action)
        elif self.version == 'v5':
            return self.v5path.format(version=self.version, api=api, action=action)
        raise ValueError('api version is un-support')

    def prepare_request(self, method, path, params=None, body: Union[dict, str] = ''):
        headers = dict()
        headers['Content-Type'] = 'application/json'
        # compose_path
        if params:
            path = f'{path}?{urlencode(params)}'
        if isinstance(body, dict):
            body = json.dumps(body)
        self.prepare_sign_headers(method, path, body, headers)
        return headers, path, body

    def get_asset(self, **kwargs):
        self.throttle = (6, 1)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('asset', 'balances'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def get_balance(self, **kwargs):
        self.throttle = (20, 2)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('account', 'balance'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def get_positions(self, **kwargs):
        self.throttle = (20, 2)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('account', 'balance'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def get_bills(self, **kwargs):
        self.throttle = (5, 1)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('account', 'bills'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def get_bills_archive(self, **kwargs):
        self.throttle = (5, 2)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('account', 'bills-archive'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def get_config(self, **kwargs):
        self.throttle = (5, 2)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('account', 'config'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def set_position_mode(self, **kwargs):
        self.throttle = (5, 2)
        method = 'POST'
        headers, path, body = self.prepare_request(method, self.find_api('account', 'config'), body=kwargs)
        return self.parse_response(self.request(method, path=path, body=body, headers=headers))

    def set_leverage(self, **kwargs):
        self.throttle = (5, 2)
        method = 'POST'
        headers, path, body = self.prepare_request(method, self.find_api('account', 'set-leverage'), body=kwargs)
        return self.parse_response(self.request(method, path=path, body=body, headers=headers))

    def get_max_size(self, **kwargs):
        self.throttle = (20, 2)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('account', 'max-size'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def get_max_avail_size(self, **kwargs):
        self.throttle = (20, 2)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('account', 'max-avail-size'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def set_margin_balance(self, **kwargs):
        self.throttle = (20, 2)
        method = 'POST'
        headers, path, body = self.prepare_request(method, self.find_api('account', 'margin-balance'), body=kwargs)
        return self.parse_response(self.request(method, path=path, body=body, headers=headers))

    def get_leverage_info(self, **kwargs):
        self.throttle = (20, 2)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('account', 'leverage-info'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def get_max_loan(self, **kwargs):
        self.throttle = (20, 2)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('account', 'max-loan'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def get_tickers(self, **kwargs):
        self.throttle = (20, 2)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('market', 'tickers'), params=kwargs)
        return self.parse_response(self.request(method, path=path, headers=headers))

    def get_ticker(self, inst_id):
        self.throttle = (20, 2)
        method = 'GET'
        headers, path, _ = self.prepare_request(method, self.find_api('market', 'ticker'), params={'instId': inst_id})
        return self.parse_response(self.request(method, path=path, headers=headers))

    def place_order(self, **kwargs):
        self.throttle = (300, 2)
        method = 'POST'
        headers, path, body = self.prepare_request(method, self.find_api('trade', 'order'), body=kwargs)
        return self.parse_response(self.request(method, path=path, body=body, headers=headers))

    def cancel_order(self, **kwargs):
        self.throttle = (60, 2)
        method = 'POST'
        headers, path, body = self.prepare_request(method, self.find_api('trade', 'cancel-order'), body=kwargs)
        return self.parse_response(self.request(method, path=path, body=body, headers=headers))
