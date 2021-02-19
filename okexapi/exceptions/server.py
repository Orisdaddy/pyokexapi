class ServerError(Exception):
    def __init__(self, status, code, message, response):
        self.status = status
        self.code = code
        self.message = message
        self.response = response

    def __str__(self):
        return f'StatusCode: {self.status}, Error Code: {self.code}, ' \
               f'Error Message: {self.message}, Response: {self.response}'
