import requests

from .exceptions.server import ServerError
from .model.request import BaseModel
from .util import *


class BaseExchange:
    host = ''
    protocol = 'https'
    _model = None
    version = None
    # 模拟
    test = False
    throtable = False
    throttle = None

    def do(self, request: BaseModel):
        self.throttle = request._throttle
        return self.request(
            request._method,
            request._path,
            request._query,
            request._body
        )

    def request(self, method, path, params=None, body=None, headers=None):
        method = method.upper()
        if not path.startswith('/'):
            path = f'/{path}'

        url = compose_url(self.protocol, self.host, path)

        # request
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=body
        )
        if not 200 <= response.status_code < 300:
            raise ServerError(
                response.status_code,
                response.json().get('code'),
                response.json().get('msg'),
                response.json()
            )

        if isinstance(self.throttle, (list, tuple)) and self.throtable:
            num, sec = self.throttle
            time.sleep(sec/num)

        return response.json()
