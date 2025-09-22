"""接口类"""
from apps.shipments import schemas


class OrderList:
    """出货订单列表"""
    def __init__(self, uid: int, filters: schemas.ShipmentsOrdersRequest):
        self.uid = uid
        self.filters = filters

    def get_list(self):
        return [self.uid, self.filters]