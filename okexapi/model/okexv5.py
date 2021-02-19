from .request import BaseModel


__all__ = (
    'GetBalance', 'GetPositions', 'GetBills', 'GetBillsArchive'
)


class GetBalance(BaseModel):
    """查看账户余额"""
    _throttle = (20, 2)
    _path = '/api/v5/account/balance'

    def __init__(
            self,
            ccy: str = None
    ):
        # 币种，如 BTC
        # 支持多币种查询（不超过20个），币种之间逗号分隔
        self.ccy = ccy
        super().__init__()


class GetPositions(BaseModel):
    """查看持仓信息"""
    _throttle = (20, 2)
    _path = '/api/v5/account/positions'

    def __init__(
            self,
            inst_type: str = None,
            inst_id: str = None,
            pos_id: str = None,
    ):
        # 产品类型
        # MARGIN：币币杠杆
        # SWAP：永续合约
        # FUTURES：交割合约
        # OPTION：期权
        # instType和instId同时传入的时候会校验instId与instType是否一致，结果返回instId的持仓信息
        self.instType = inst_type

        # 产品ID，如 BTC-USD-190927-5000-C
        self.instId = inst_id

        # 持仓ID
        # 支持多个posId查询（不超过20个），逗号分割
        self.posId = pos_id
        super().__init__()


class GetBills(BaseModel):
    """账单流水查询（近七天）"""
    _throttle = (5, 1)
    _path = '/api/v5/account/bills'

    def __init__(
            self,
            inst_type: str = None,
            ccy: str = None,
            mgn_mode: str = None,
            ct_type: str = None,
            type: str = None,
            sub_type: str = None,
            after: str = None,
            before: str = None,
            limit: str = None,
    ):
        self.instType = inst_type
        self.ccy = ccy
        self.mgnMode = mgn_mode
        self.ctType = ct_type
        self.type = type
        self.subType = sub_type
        self.after = after
        self.before = before
        self.limit = limit
        super().__init__()


class GetBillsArchive(BaseModel):
    """账单流水查询（近三个月）"""
    _throttle = (5, 2)
    _path = '/api/v5/account/bills-archive'

    def __init__(
            self,
            inst_type: str = None,
            ccy: str = None,
            mgn_mode: str = None,
            ct_type: str = None,
            type: str = None,
            sub_type: str = None,
            after: str = None,
            before: str = None,
            limit: str = None,
    ):
        self.instType = inst_type
        self.ccy = ccy
        self.mgnMode = mgn_mode
        self.ctType = ct_type
        self.type = type
        self.subType = sub_type
        self.after = after
        self.before = before
        self.limit = limit
        super().__init__()

