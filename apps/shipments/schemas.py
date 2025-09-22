"""
schemas.py模块
    数据序列化和反序列化，数据验证
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, List, Literal


class ShipmentsOrdersRequest(BaseModel):
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
    shippingDate: Optional[List[str]] = Field(default=None, title="发货日期")
    departureDate: Optional[List[str]] = Field(default=None, title="开船日期")
    portArrivalDate: Optional[List[str]] = Field(default=None, title="到港日期")
    deliveryDate: Optional[List[str]] = Field(default=None, title="派送日期")
    signedDate: Optional[List[str]] = Field(default=None, title="签收日期")

class ShipmentItem(BaseModel):
    """内容列表中的货件条目"""
    orderCode: str = Field(default=None,title="订单号")
    firstLegTrackingNumber: str = Field(default=None,title="头程追踪号")
    lastMileTrackingNumber: str = Field(default=None,title="尾程跟踪号")
    countryCode: str = Field(default=None,title="目的国家")
    warehouseCode: str = Field(default=None,title="仓库代码")
    shipmentName: str = Field(default=None,title="货件名称")

class ShipmentsOrdersResponse(BaseModel):
    """出货单管理-出货单列表响应体"""
    code: Optional[int] = Field(default=0, title="返回码")
    message: Optional[str] = Field(default="SUCCESS", title="返回信息")
    result: Optional[Any] = Field(default={}, title="返回结果数据")

class ShipmentsOrdersResult(BaseModel):
    """返回具体信息的结构"""
    totalElements: int = Field(default=None,title="符合条件的总记录数")
    totalPages: int = Field(default=None,title="总页数")
    pageSize: int = Field(default=None,title="页面列表数大小")
    pageNum: int = Field(default=None,title="页码数")
    content: List[ShipmentItem] = Field(default=None,title="内容列表")


class Response(BaseModel):
    """响应体"""
    # Optional 是 Union[int, None] 的简写 Optional[int]允许为整数或None
    code: Optional[int] = Field(default=0, title="返回码")
    message: Optional[str] = Field(default="SUCCESS", title="返回信息")
    result: Optional[Any] = Field(default={}, title="返回结果数据")