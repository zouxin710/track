"""
schemas.py模块
    数据序列化和反序列化，数据验证
"""
import math
from datetime import datetime

from pydantic import  Field
from typing import Optional, Any, List, Literal

from apps.schemas import BaseModelWithORM


class ShipmentsOrdersRequest(BaseModelWithORM):
    """出货单管理-出货单列表请求体"""
    # Field()是 Pydantic中用来声明字段属性的方式
    pageSize: int = Field(default=10, title="每页的大小")
    pageNum: int = Field(default=1, title="当前页码")

    # 查询条件
    orderCode: Optional[str] = Field(default=None, title="订单号")
    firstLegTrackingNumber: Optional[str] = Field(default=None, title="头程追踪号")
    lastMileTrackingNumber: Optional[str] = Field(default=None, title="尾程追踪号")
    shipmentName: Optional[str] = Field(default=None, title="货件名称")

    shippingStatus: Optional[
        Literal["SHIPPED", "DEPARTURE", "ARRIVED", "DELIVERY", "SIGNED", "SHELVED"]
    ] = Field(default=None, title="物流状态")

    shippingMethod: Optional[str] = Field(default=None, title="运输方式")
    providerCode: Optional[str] = Field(default=None, title="物流商")
    countryCode: Optional[str] = Field(default=None, title="目的国家")
    isException: Optional[bool] = Field(default=None, title="订单是否异常")
    warehouseCode: Optional[str] = Field(default=None, title="仓库代码")

    # 日期条件（字符串数组）
    shippingDate: Optional[List[datetime]] = Field(default=None, title="发货日期")
    departureDate: Optional[List[datetime]] = Field(default=None, title="开船日期")
    portArrivalDate: Optional[List[datetime]] = Field(default=None, title="到港日期")
    deliveryDate: Optional[List[datetime]] = Field(default=None, title="派送日期")
    signedDate: Optional[List[datetime]] = Field(default=None, title="签收日期")

class ShipmentsOrderDetailRequest(BaseModelWithORM):
    """出货单管理-出货单详情请求体"""
    orderCode: str = Field(..., title="订单号")

class PaginationResponse(BaseModelWithORM):
    """分页应答体"""
    totalElements: int = Field(..., title="符合条件的总记录数")
    totalPages: int = Field(default=1, title="总页数")
    pageSize: int = Field(..., title="每页的大小")
    pageNum: int = Field(..., title="当前页码")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.totalPages = math.ceil(self.totalElements / self.pageSize)
class ShipmentItem(BaseModelWithORM):
    """订单列表中要返回的的货件条目"""
    orderCode: str = Field(...,title="订单号",alias="order_code")# ...表示该字段必填
    firstLegTrackingNumber: str = Field(...,title="头程追踪号",alias="first_leg_tracking_number")
    lastMileTrackingNumber: str = Field(...,title="尾程跟踪号",alias="last_mile_tracking_number")
    countryCode: Optional[str] = Field(default=None,title="目的国家",alias="country_code")
    warehouseCode: Optional[str] = Field(default=None,title="仓库代码",alias="warehouse_code")
    shipmentName: Optional[str] = Field(default=None,title="货件名称",alias="shipment_name")
    providerCode: Optional[str] = Field(default=None,title="物流商",alias="provider_code")
    shippingChannel: Optional[str] = Field(default=None,title="物流渠道",alias="shipping_channel")
    shippingMethod: Optional[str] = Field(default=None,title="运输方式",alias="shipping_method")
    boxNum : Optional[int] = Field(default=None,title="箱数",alias="box_num")
    shippingDate :Optional[datetime] = Field(default=None,title="发货日期",alias="shipping_date")
    departureDate :Optional[datetime] = Field(default=None,title="开船日期",alias="departure_date")
    portArrivalDate :Optional[datetime] = Field(default=None,title="到港日期",alias="port_arrival_date")
    deliveryDate :Optional[datetime] = Field(default=None,title="派送日期",alias="delivery_date")
    signedDate :Optional[datetime] = Field(default=None,title="签收日期",alias="signed_date")
    signedNum : Optional[int] = Field(default=None,title="已签收数",alias="signed_num")
    shelvedTime :Optional[datetime] = Field(default=None,title="上架完成时间",alias="shelved_time")
    isException :Optional[int] = Field(default=None,title="订单是否异常",alias="is_exception")
    createTime :Optional[datetime] = Field(default=None,title="创建时间,导入系统时间",alias="create_time")

# class ShipmentsOrdersResponse(BaseModel):
#     """出货单管理-出货单列表响应体"""
#     # Optional 是 Union[int, None] 的简写 Optional[int]允许为整数或None
#     code: Optional[int] = Field(default=0, title="返回码")
#     message: Optional[str] = Field(default="SUCCESS", title="返回信息")
#     result: Optional[Any] = Field(default={}, title="返回结果数据")


class ShipmentsOrdersResult(PaginationResponse):
    """返回具体信息的结构"""
    content: List[ShipmentItem] = Field(default=None,title="内容列表")


class Response(BaseModelWithORM):
    """响应体"""
    code: Optional[int] = Field(default=0, title="返回码")
    message: Optional[str] = Field(default="SUCCESS", title="返回信息")
    result: Optional[Any] = Field(default={}, title="返回结果数据")
