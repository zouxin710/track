"""
schemas.py模块
    数据序列化和反序列化，数据验证
"""
import math
from datetime import datetime
from decimal import Decimal

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


class ShipmentExceptionsRequest(BaseModelWithORM):
    """异常列表请求体"""
    orderCode: Optional[str] = Field(default=None, title="订单号")
    firstLegTrackingNumber: Optional[str] = Field(default=None, title="头程追踪号")
    shipmentName: Optional[str] = Field(default=None, title="货件名称")
    exceptionType:Optional[str] = Field(default=None, title="异常类型")
    exceptionNode: Optional[str] = Field(default=None, title="异常节点")
    exceptionDate: Optional[List[datetime]] = Field(default=None, title="触发时间(我们系统计算的时间)")

# class ShipmentsOrderDetailRequest(BaseModelWithORM):
#     """出货单管理-出货单详情请求体"""
#     orderCode: str = Field(..., title="订单号")

class PaginationResponse(BaseModelWithORM):
    """分页应答体"""
    totalElements: int = Field(..., title="符合条件的总记录数")
    totalPages: int = Field(default=1, title="总页数")
    pageSize: int = Field(..., title="每页的大小")
    pageNum: int = Field(..., title="当前页码")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.totalPages = math.ceil(self.totalElements / self.pageSize)
class ShipmentOrdersItem(BaseModelWithORM):
    """出货单管理-订单列表中要返回的的货件条目"""
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

class ShipmentsOrdersResult(PaginationResponse):
    """出货单管理-返回具体信息的结构"""
    content: List[ShipmentOrdersItem] = Field(default=None,title="内容列表")


class ShipmentDetailItem(BaseModelWithORM):
    """出货单管理-订单详情页中要返回的的货件条目"""
    orderCode: str = Field(...,title="订单号",alias="order_code")# ...表示该字段必填
    firstLegTrackingNumber: str = Field(...,title="头程追踪号",alias="first_leg_tracking_number")
    lastMileTrackingNumber: str = Field(...,title="尾程跟踪号",alias="last_mile_tracking_number")
    shipmentName: Optional[str] = Field(default=None,title="货件名称",alias="shipment_name")
    warehouseCode: Optional[str] = Field(default=None,title="仓库代码",alias="warehouse_code")
    addTime :Optional[datetime] = Field(default=None,title="创建时间",alias="add_time")
    providerCode : Optional[str] = Field(default=None,title="物流商",alias="provider_code")
    boxNum : Optional[int] = Field(default=None,title="箱数",alias="box_num")
    shippingChannel : Optional[str] = Field(default=None,title="物流渠道",alias="shipping_channel")
    shippingMethod : Optional[str] = Field(default=None,title="运输方式",alias="shipping_method")
    countryCode : Optional[str] = Field(default=None,title="目的国家",alias="country_code")
    weight : Optional[Decimal] = Field(default=None,title="重量",alias="weight")
    volumeWeight : Optional[Decimal] = Field(default=None,title="体积重",alias="volume_weight")
    billingHeavy : Optional[Decimal] = Field(default=None,title="计费重",alias="billing_heavy")
    price : Optional[Decimal] = Field(default=None,title="单价",alias="price")
    freight : Optional[Decimal] = Field(default=None,title="运费",alias="freight")
    totalCost : Optional[Decimal] = Field(default=None,title="合计费用",alias="total_cost")
    providerCost : Optional[Decimal] = Field(default=None,title="物流商费用",alias="provider_cost")
    customsDuty : Optional[Decimal] = Field(default=None,title="关税",alias="customs_duty")
    clearanceFee : Optional[Decimal] = Field(default=None,title="清关费",alias="clearance_fee")
    extraCategoryFee : Optional[Decimal] = Field(default=None,title="附加费",alias="extra_category_fee")
    superProductFee : Optional[Decimal] = Field(default=None,title="超品名费",alias="super_product_fee")
    deduction : Optional[Decimal] = Field(default=None,title="扣减",alias="deduction")
    costDifference : Optional[Decimal] = Field(default=None,title="费用差异",alias="cost_difference")
    shippingStatus : Optional[str] = Field(default=None,title="物流状态",alias="shipping_status")
    shippingDate :Optional[datetime] = Field(default=None,title="发货日期",alias="shipping_date")
    departureDate :Optional[datetime] = Field(default=None,title="开船日期",alias="departure_date")
    portArrivalDate :Optional[datetime] = Field(default=None,title="到港日期",alias="port_arrival_date")
    deliveryDate :Optional[datetime] = Field(default=None,title="派送日期",alias="delivery_date")
    signedDate :Optional[datetime] = Field(default=None,title="最早签收日期",alias="signed_date")
    shelvedTime :Optional[datetime] = Field(default=None,title="上架完成时间",alias="shelved_time")
    signedNum : Optional[int] = Field(default=None,title="已签收数量",alias="signed_num")
    totalTrack : Optional[str] = Field(default=None,title="头程完整轨迹",alias="total_tracking_number")
    shippingDays : Optional[int] = Field(default=None,title="已发货天数",alias="shipping_days")
    warehouseAging : Optional[int] = Field(default=None,title="仓库时效",alias="warehouse_aging")
    navigationAging : Optional[int] = Field(default=None,title="航行时效",alias="navigation_aging")
    portDeliveryDate:Optional[int] = Field(default=None,title="到港派送时效",alias="port_delivery_date")
    deliveryAcceptAging : Optional[int] = Field(default=None,title="签收时效",alias="delivery_accept_aging")
    shelfAging : Optional[int] = Field(default=None,title="上架时效",alias="shelf_aging")
    remark : Optional[str] = Field(default=None,title="其他(业务备注)",alias="remark")
    isException : Optional[int] = Field(default=None,title="订单是否异常",alias="is_exception")

class ProviderTrackingItem(BaseModelWithORM):
    """物流商原始轨迹节点"""
    trackTime: Optional[datetime] = Field(...,title="轨迹时间",alias="track_time")
    trackContent: Optional[str] = Field(...,title="原文信息",alias="track_content")


class ProviderTrackingResult(BaseModelWithORM):
    """物流商原始轨迹节点列表"""
    nodes: List[ProviderTrackingItem] = Field(...,title="轨迹节点")

class Response(BaseModelWithORM):
    """响应体"""
    code: Optional[int] = Field(default=200, title="返回码")
    message: Optional[str] = Field(default="SUCCESS", title="返回信息")
    result: Optional[Any] = Field(default={}, title="返回结果数据")
