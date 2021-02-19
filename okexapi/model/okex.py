from .request import BaseModel


class GetBalance(BaseModel):
    def __init__(
            self,
            ccy: str = None
    ):
        self.path = '/api/v5/account/balance'
        self.ccy = ccy
        super().__init__()
