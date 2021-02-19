import time
import datetime


def get_date():
    now = datetime.datetime.utcnow()
    return int(time.mktime(now.timetuple())), now.strftime('%Y-%m-%dT%H:%M:%SZ')


def compose_url(protocol: str, host: str, path: str):
    if not path.startswith('/'):
        path = f'/{path}'
    if not protocol.endswith('://'):
        protocol += '://'
    return f'{protocol}{host}{path}'
