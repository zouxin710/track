"""接口类"""
from apps.shipments.schemas import *


class OrderList:
    """出货订单列表"""
    def __init__(self, uid: int, filters: ShipmentsOrdersRequest):
        self.uid = uid
        self.filters = filters

    def get_list(self):
        response_content = ShipmentsOrdersResult(content=[ShipmentItem()])
        return response_content