import json


class BaseModel:
    _method = 'GET'
    # (次数, 每秒)
    _throttle = (20, 2)
    _path = None
    _query = None
    _body = None

    def __init__(self):
        data = self._parse()
        tmp = {k: v for k, v in data.items() if v is not None}

        if self._method.upper() == 'GET':
            self._query = tmp
        elif self._method.upper() == 'POST':
            self._body = json.dumps(tmp)

    def _parse(self):
        tmp = dict()
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                tmp[k] = v
        return tmp
