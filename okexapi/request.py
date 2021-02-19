class Request:
    def __init__(
            self,
            method=None,
            path=None,
            query=None,
            body=None
    ):
        self.method = method
        self.path = path
        self.query = query
        self.body = body
