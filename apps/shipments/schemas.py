"""
schemas.py模块
    数据序列化和反序列化，数据验证
"""
import math
from datetime import datetime
from decimal import Decimal
from typing import Optional, Any, List

from pydantic import Field

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
    shippingStatus: Optional[str] = Field(default=None, title="物流状态")
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


class ShipmentsOrderUpdateRequest(BaseModelWithORM):
    """出货单管理-出货单更新请求体"""
    firstLegTrackingNumber: str = Field(..., title="头程追踪号", alias="first_leg_tracking_number")
    lastMileTrackingNumber: str = Field(..., title="尾程追踪号", alias="last_mile_tracking_number")
    shipmentName: str = Field(..., title="货件名称", alias="shipment_name")
    warehouseCode: str = Field(..., title="仓库代码", alias="warehouse_code")
    addTime: str = Field(..., title="创建时间", alias="add_time")
    providerCode: str = Field(..., title="物流商", alias="provider_code")
    boxNum: str = Field(..., title="箱数", alias="box_num")
    shippingChannel: str = Field(..., title="物流渠道", alias="shipping_channel")
    shippingMethod: str = Field(..., title="运输方式", alias="shipping_method")
    countryCode: str = Field(..., title="目的国家", alias="country_code")
    weight: Decimal = Field(..., title="重量", alias="weight")
    volumeWeight: Decimal = Field(..., title="体积重", alias="volume_weight")
    billingHeavy: Decimal = Field(..., title="计费重", alias="billing_heavy")
    price: Decimal = Field(..., title="单价", alias="price")
    freight: Decimal = Field(..., title="运费", alias="freight")
    totalCost: Decimal = Field(..., title="合计费用", alias="total_cost")
    providerCost: Decimal = Field(..., title="物流商费用", alias="provider_cost")
    customsDuty: Decimal = Field(..., title="关税", alias="customs_duty")
    clearanceFee: Decimal = Field(..., title="清关费", alias="clearance_fee")
    extraCategoryFee: Decimal = Field(..., title="附加费", alias="extra_category_fee")
    superProductFee: Decimal = Field(..., title="超品名费", alias="super_product_fee")
    deduction: Decimal = Field(..., title="扣减", alias="deduction")
    costDifference: Decimal = Field(..., title="费用差异", alias="cost_difference")


class ShipmentsTrackingRequest(BaseModelWithORM):
    """头程轨迹跟踪-头程轨迹所有节点请求体"""
    identifyStatus: Optional[str] = Field(default=None, title="审核状态", alias="identify_status")


class ShipmentsPendingRequest(BaseModelWithORM):
    """头程轨迹跟踪-轨迹订单节点列表请求体"""
    pageSize: int = Field(default=10, title="每页的大小")
    pageNum: int = Field(default=1, title="当前页码")
    shipmentName: Optional[str] = Field(default=None, title="货件名称")
    providerCode: Optional[str] = Field(default=None, title="物流商")
    orderCode: Optional[str] = Field(default=None, title="订单号")
    isPending: Optional[bool] = Field(default=False, title="是否待审核")


class ShipmentsReviewPostRequest(BaseModelWithORM):
    """头程轨迹跟踪-审核提交请求体"""
    artificialTrackType: str = Field(..., title="人工轨迹类型", alias="artificial_track_type")
    artificialTrackNode: str = Field(..., title="人工轨迹节点", alias="artificial_track_node")
    artificialNodeDate: datetime = Field(..., title="人工节点时间", alias="artificial_node_date")


class ShipmentsAddNodeRequest(BaseModelWithORM):
    """头程轨迹跟踪-添加节点请求体"""
    orderCode: str = Field(..., title="订单号", alias="order_code")
    trackContent: str = Field(..., title="人工轨迹文本说明", alias="track_content")
    artificialTrackType: str = Field(..., title="人工轨迹类型", alias="artificial_track_type")
    artificialTrackNode: str = Field(..., title="人工轨迹节点", alias="artificial_track_node")
    artificialNodeDate: datetime = Field(..., title="人工节点时间", alias="artificial_node_date")


class ShipmentsExceptionsRequest(BaseModelWithORM):
    """异常处置-异常列表请求体"""
    pageSize: int = Field(default=10, title="每页的大小")
    pageNum: int = Field(default=1, title="当前页码")
    orderCode: Optional[str] = Field(default=None, title="订单号")
    firstLegTrackingNumber: Optional[str] = Field(default=None, title="头程追踪号")
    shipmentName: Optional[str] = Field(default=None, title="货件名称")
    exceptionType: Optional[str] = Field(default=None, title="异常类型")
    exceptionNode: Optional[str] = Field(default=None, title="异常节点")
    exceptionDate: Optional[List[datetime]] = Field(default=None, title="触发时间(我们系统计算的时间)")
    status: Optional[List[str]] = Field(default=None, title="触发时间(我们系统计算的时间)")


class ShipmentsExceptionsProcessingRequest(BaseModelWithORM):
    """异常处置-异常处置操作body参数"""
    content: str = Field(..., title="异常处理内容")
    status: str = Field(..., title="异常处置状态")


class ShipmentsExceptionsLogsRequest(BaseModelWithORM):
    """异常处置-异常处理日志列表请求体"""
    pageSize: int = Field(default=10, title="每页的大小")
    pageNum: int = Field(default=1, title="当前页码")
    exceptionId: Optional[int] = Field(default=None, title="异常ID")
    orderCode: Optional[str] = Field(default=None, title="订单号")
    firstLegTrackingNumber: Optional[str] = Field(default=None, title="头程追踪号")
    shipmentName: Optional[str] = Field(default=None, title="货件名称")


class PaginationResponse(BaseModelWithORM):
    """分页应答体"""
    totalElements: int = Field(..., title="符合条件的总记录数")
    totalPages: int = Field(default=1, title="总页数")
    pageSize: int = Field(..., title="每页的大小")
    pageNum: int = Field(..., title="当前页码")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.totalPages = math.ceil(self.totalElements / self.pageSize)


class ShipmentsOrdersItem(BaseModelWithORM):
    """出货单管理-订单列表中要返回的的货件字段"""
    orderCode: str = Field(..., title="订单号", alias="order_code")  # ...表示该字段必填
    firstLegTrackingNumber: str = Field(..., title="头程追踪号", alias="first_leg_tracking_number")
    lastMileTrackingNumber: str = Field(..., title="尾程跟踪号", alias="last_mile_tracking_number")
    countryCode: Optional[str] = Field(default=None, title="目的国家", alias="country_code")
    warehouseCode: Optional[str] = Field(default=None, title="仓库代码", alias="warehouse_code")
    shipmentName: Optional[str] = Field(default=None, title="货件名称", alias="shipment_name")
    providerCode: Optional[str] = Field(default=None, title="物流商", alias="provider_code")
    shippingChannel: Optional[str] = Field(default=None, title="物流渠道", alias="shipping_channel")
    shippingMethod: Optional[str] = Field(default=None, title="运输方式", alias="shipping_method")
    shippingStatus: Optional[str] = Field(default=None, title="物流状态", alias="shipping_status")
    boxNum: Optional[int] = Field(default=None, title="箱数", alias="box_num")
    shippingDate: Optional[datetime] = Field(default=None, title="发货日期", alias="shipping_date")
    departureDate: Optional[datetime] = Field(default=None, title="开船日期", alias="departure_date")
    portArrivalDate: Optional[datetime] = Field(default=None, title="到港日期", alias="port_arrival_date")
    deliveryDate: Optional[datetime] = Field(default=None, title="派送日期", alias="delivery_date")
    signedDate: Optional[datetime] = Field(default=None, title="签收日期", alias="signed_date")
    signedNum: Optional[int] = Field(default=None, title="已签收数", alias="signed_num")
    shelvedTime: Optional[datetime] = Field(default=None, title="上架完成时间", alias="shelved_time")
    isException: Optional[int] = Field(default=None, title="订单是否异常", alias="is_exception")
    createTime: Optional[datetime] = Field(default=None, title="创建时间,导入系统时间", alias="create_time")


class ShipmentsOrdersResult(PaginationResponse):
    """
    出货单管理-返回具体信息的结构
    content存储内容列表 该类继承分页响应体 创建时带上分页参数
    """
    content: List[ShipmentsOrdersItem] = Field(default=None, title="内容列表")


class ShipmentsDetailItem(BaseModelWithORM):
    """出货单管理-订单详情页中要返回的的字段"""
    orderCode: str = Field(..., title="订单号", alias="order_code")  # ...表示该字段必填
    firstLegTrackingNumber: str = Field(..., title="头程追踪号", alias="first_leg_tracking_number")
    lastMileTrackingNumber: str = Field(..., title="尾程跟踪号", alias="last_mile_tracking_number")
    shipmentName: Optional[str] = Field(default=None, title="货件名称", alias="shipment_name")
    warehouseCode: Optional[str] = Field(default=None, title="仓库代码", alias="warehouse_code")
    addTime: Optional[datetime] = Field(default=None, title="创建时间", alias="add_time")
    providerCode: Optional[str] = Field(default=None, title="物流商", alias="provider_code")
    boxNum: Optional[int] = Field(default=None, title="箱数", alias="box_num")
    shippingChannel: Optional[str] = Field(default=None, title="物流渠道", alias="shipping_channel")
    shippingMethod: Optional[str] = Field(default=None, title="运输方式", alias="shipping_method")
    countryCode: Optional[str] = Field(default=None, title="目的国家", alias="country_code")
    weight: Optional[Decimal] = Field(default=None, title="重量", alias="weight")
    volumeWeight: Optional[Decimal] = Field(default=None, title="体积重", alias="volume_weight")
    billingHeavy: Optional[Decimal] = Field(default=None, title="计费重", alias="billing_heavy")
    price: Optional[Decimal] = Field(default=None, title="单价", alias="price")
    freight: Optional[Decimal] = Field(default=None, title="运费", alias="freight")
    totalCost: Optional[Decimal] = Field(default=None, title="合计费用", alias="total_cost")
    providerCost: Optional[Decimal] = Field(default=None, title="物流商费用", alias="provider_cost")
    customsDuty: Optional[Decimal] = Field(default=None, title="关税", alias="customs_duty")
    clearanceFee: Optional[Decimal] = Field(default=None, title="清关费", alias="clearance_fee")
    extraCategoryFee: Optional[Decimal] = Field(default=None, title="附加费", alias="extra_category_fee")
    superProductFee: Optional[Decimal] = Field(default=None, title="超品名费", alias="super_product_fee")
    deduction: Optional[Decimal] = Field(default=None, title="扣减", alias="deduction")
    costDifference: Optional[Decimal] = Field(default=None, title="费用差异", alias="cost_difference")
    shippingStatus: Optional[str] = Field(default=None, title="物流状态", alias="shipping_status")
    shippingDate: Optional[datetime] = Field(default=None, title="发货日期", alias="shipping_date")
    departureDate: Optional[datetime] = Field(default=None, title="开船日期", alias="departure_date")
    portArrivalDate: Optional[datetime] = Field(default=None, title="到港日期", alias="port_arrival_date")
    deliveryDate: Optional[datetime] = Field(default=None, title="派送日期", alias="delivery_date")
    signedDate: Optional[datetime] = Field(default=None, title="最早签收日期", alias="signed_date")
    shelvedTime: Optional[datetime] = Field(default=None, title="上架完成时间", alias="shelved_time")
    signedNum: Optional[int] = Field(default=None, title="已签收数量", alias="signed_num")
    totalTrack: Optional[str] = Field(default=None, title="头程完整轨迹", alias="total_tracking_number")
    shippingDays: Optional[int] = Field(default=None, title="已发货天数", alias="shipping_days")
    warehouseAging: Optional[int] = Field(default=None, title="仓库时效", alias="warehouse_aging")
    navigationAging: Optional[int] = Field(default=None, title="航行时效", alias="navigation_aging")
    portDeliveryDate: Optional[int] = Field(default=None, title="到港派送时效", alias="port_delivery_date")
    deliveryAcceptAging: Optional[int] = Field(default=None, title="签收时效", alias="delivery_accept_aging")
    shelfAging: Optional[int] = Field(default=None, title="上架时效", alias="shelf_aging")
    remark: Optional[str] = Field(default=None, title="其他(业务备注)", alias="remark")
    isException: Optional[int] = Field(default=None, title="订单是否异常", alias="is_exception")


class ShipmentsTrackingItem(BaseModelWithORM):
    """头程轨迹跟踪-当前订单号的所有轨迹节点字段"""
    id: int = Field(..., title="id", alias="id")
    trackTime: datetime = Field(..., title="轨迹时间", alias="track_time")
    trackContent: str = Field(..., title="轨迹原文", alias="track_content")
    trackType: Optional[str] = Field(default=None, title="AI轨迹类型", alias="track_type")
    trackNode: Optional[str] = Field(default=None, title="AI轨迹节点", alias="track_node")
    nodeDate: Optional[datetime] = Field(default=None, title="AI节点时间", alias="node_date")
    confidence: Optional[Decimal] = Field(default=None, title="AI识别置信度", alias="confidence")
    identifyStatus: Optional[str] = Field(default=None, title="审核状态", alias="identify_status")
    artificialReviewTime: Optional[datetime] = Field(default=None, title="人工审核时间", alias="artificial_review_time")
    artificialTrackType: Optional[str] = Field(default=None, title="人工审核后的最终轨迹类型", alias="artificial_track_type")
    artificialTrackNode: Optional[str] = Field(default=None, title="人工审核后的最终节点", alias="artificial_track_node")
    artificialNodeDate: Optional[datetime] = Field(default=None, title="人工审核后的最终节点时间", alias="artificial_node_date")
    source: Optional[int] = Field(default=None, title="节点来源", alias="source")


class ShipmentsTrackingResult(BaseModelWithORM):
    """头程轨迹跟踪-当前订单号所有轨迹节点返回响应体"""
    nodeCount: Optional[int] = Field(default=0, title="当前节点数量")
    nodes: List[ShipmentsTrackingItem] = Field(..., title="轨迹节点")


class ShipmentsPendingItem(BaseModelWithORM):
    """头程轨迹跟踪-待审核列表的响应体字段"""
    orderCode: str = Field(..., title="订单号", alias="order_code")
    shipmentName: Optional[str] = Field(default=None, title="货件名称", alias="shipment_name")
    firstLegTrackingNumber: str = Field(..., title="头程追踪号", alias="first_leg_tracking_number")
    lastMileTrackingNumber: Optional[str] = Field(default=None, title="尾程追踪号", alias="last_mile_tracking_number")
    providerCode: Optional[str] = Field(default=None, title="物流商", alias="provider_code")
    shippingChannel: Optional[str] = Field(default=None, title="物流渠道", alias="shipping_channel")
    latestTrackTime: Optional[datetime] = Field(default=None, title="最新轨迹时间", alias="latest_track_time")
    pendingCount: int = Field(default=0, title="待审核数量", alias="pending_count")


class ShipmentsPendingResult(PaginationResponse):
    """头程轨迹跟踪-待审核列表的响应体"""
    content: List[ShipmentsPendingItem] = Field(..., title="内容列表")


class ExceptionsItem(BaseModelWithORM):
    """异常处置管理-异常列表中要返回的的字段 这些字段存在异常表中"""
    exceptionId: int = Field(..., title="异常id", alias="exception_id")
    orderCode: str = Field(..., title="订单号", alias="order_code")  # ...表示该字段必填
    exceptionType: str = Field(..., title="异常类型", alias="exception_type")
    exceptionNode: str = Field(..., title="异常节点", alias="exception_node")
    exceptionDate: datetime = Field(..., title="触发时间", alias="exception_date")
    status: str = Field(..., title="处置状态", alias="status")
    updateTime: datetime = Field(..., title="最新更新时间", alias="update_time")


class ExceptionsJoinItem(BaseModelWithORM):
    """异常处置管理-异常列表中要返回的的字段 这些字段关联在order订单表中"""
    providerCode: Optional[str] = Field(default=None, title="物流商", alias="provider_code")
    shipmentName: Optional[str] = Field(default=None, title="货件名称", alias="shipment_name")
    firstLegTrackingNumber: Optional[str] = Field(default=None, title="头程追踪号", alias="first_leg_tracking_number")


class ShipmentsExceptionsItem(ExceptionsItem, ExceptionsJoinItem):
    """异常处置管理-返回具体信息的结构"""
    pass


class ShipmentsExceptionsResult(PaginationResponse):
    """异常处置管理-返回具体信息的结构"""
    content: List[ShipmentsExceptionsItem] = Field(default=None, title="内容列表")


class ExceptionLogsItem(BaseModelWithORM):
    """异常处置记录-异常记录表中可以查询到的需求字段"""
    id: int = Field(..., title="处理记录id", alias="id")
    status: str = Field(..., title="异常处置状态", alias="status")
    content: str = Field(..., title="处置记录", alias="operation")
    operatorName: str = Field(..., title="处置人姓名", alias="operator_name")


class ExceptionLogsJoinInfoItem(BaseModelWithORM):
    """异常处置记录-这个字段关联在order订单表中"""
    firstLegTrackingNumber: Optional[str] = Field(default=None, title="头程追踪号", alias="first_leg_tracking_number")
    shipmentName: Optional[str] = Field(default=None, title="货件名称", alias="shipment_name")


class ExceptionLogsJoinExceptionItem(BaseModelWithORM):
    """异常处置记录-这个字段关联在异常信息中"""
    exceptionType: Optional[str] = Field(default=None, title="异常类型", alias="exception_type")
    exceptionNode: Optional[str] = Field(default=None, title="异常节点", alias="exception_node")
    createTime: Optional[datetime] = Field(default=None, title="异常触发时间", alias="create_time")


class ShipmentsExceptionLogsItem(ExceptionLogsItem, ExceptionLogsJoinInfoItem, ExceptionLogsJoinExceptionItem):
    """异常处置记录-返回具体信息的结构"""
    pass


class ShipmentsExceptionLogsResult(PaginationResponse):
    """异常处置记录-异常处置记录列表的返回响应体"""
    content: List[ShipmentsExceptionLogsItem] = Field(default=None, title="内容列表")


class Response(BaseModelWithORM):
    """响应体"""
    code: Optional[int] = Field(default=0, title="返回码")
    message: Optional[str] = Field(default="SUCCESS", title="返回信息")
    result: Optional[Any] = Field(default={}, title="返回结果数据")
