"""接口类"""
from functools import cached_property

from apps.models import ShipmentOrderInfo
from apps.shipments import schemas
from apps.shipments.schemas import *


class OrderList:
    """出货订单列表"""
    def __init__(self, filters: ShipmentsOrdersRequest):
        # 初始化实例时 传入请求体filters
        self.filters = filters

    def get_list(self):
        """获取列表数据"""
        pagination = schemas.PaginationResponse(
            totalElements=self.get_total(),
            pageNum=self.filters.pageNum,
            pageSize=self.filters.pageSize,
        )
        # print(pagination.totalPages) # 2
        # print(pagination) # totalElements=20 totalPages=2 pageSize=10 pageNum=1
        # print(pagination.model_dump_json()) # json字符串
        # print(pagination.model_dump()) # dict

        # 拿列表
        # 判断 如果传入的页码数 > 总页数  则返回空列表
        if self.filters.pageNum > pagination.totalPages:
            details = []
        else:
            details = self.get_details()
        # **pagination.model_dump() 将字典解包为关键字参数
        # ShipmentsOrdersResult返回内容列表content,分页信息
        return ShipmentsOrdersResult(content=details, **pagination.model_dump())

    def get_total(self) -> int:
        """拿取查询的结果总数"""
        return self.query.count()

    def get_details(self) -> list:
        """拿取查询的结果详情"""
        query = self.query.order_by(ShipmentOrderInfo.create_time.desc()).paginate(self.filters.pageNum, self.filters.pageSize)
        records = []
        for q in query:
            order = schemas.ShipmentItem.model_validate(q)
            recode = schemas.ShipmentItem(**order.model_dump())
            records.append(recode)
        return records

    # 再在 query 上追加 order + paginate
    # query = query.order_by(ShipmentOrderInfo.create_time.desc()).paginate(f.pageNum or 1, f.pageSize or 10)
    # print(4,query.dicts())
    # rows = list(query.dicts())
    # print(rows)
    @cached_property
    def query(self):
        """查询数据库操作"""
        query = ShipmentOrderInfo.select(
     ShipmentOrderInfo.order_code,
            ShipmentOrderInfo.first_leg_tracking_number,
            ShipmentOrderInfo.last_mile_tracking_number,
            ShipmentOrderInfo.country_code,
            ShipmentOrderInfo.warehouse_code,
            ShipmentOrderInfo.shipment_name,
            ShipmentOrderInfo.provider_code,
            ShipmentOrderInfo.shipping_channel,
            ShipmentOrderInfo.shipping_method,
            ShipmentOrderInfo.box_num,
            ShipmentOrderInfo.shipping_date,
            ShipmentOrderInfo.departure_date,
            ShipmentOrderInfo.port_arrival_date,
            ShipmentOrderInfo.delivery_date,
            ShipmentOrderInfo.signed_date,
            ShipmentOrderInfo.signed_num,
            ShipmentOrderInfo.shelved_time,
            ShipmentOrderInfo.is_exception,
            ShipmentOrderInfo.create_time
        )

        f = self.filters
        # 字符串精确匹配条件
        if f.orderCode:
            query = query.where(ShipmentOrderInfo.order_code == f.orderCode)
        if f.firstLegTrackingNumber:
            query = query.where(ShipmentOrderInfo.first_leg_tracking_number == f.firstLegTrackingNumber)
        if f.lastMileTrackingNumber:
            query = query.where(ShipmentOrderInfo.last_mile_tracking_number == f.lastMileTrackingNumber)
        if f.shipmentName:
            query = query.where(ShipmentOrderInfo.shipment_name == f.shipmentName)
        if f.providerCode:
            query = query.where(ShipmentOrderInfo.provider_code == f.providerCode)
        if f.shippingMethod:
            query = query.where(ShipmentOrderInfo.shipping_method == f.shippingMethod)
        if f.countryCode:
            query = query.where(ShipmentOrderInfo.country_code == f.countryCode)
        if f.warehouseCode:
            query = query.where(ShipmentOrderInfo.warehouse_code == f.warehouseCode)

        # 布尔值条件
        if f.isException is not None:  # 注意这里要区分None和False
            query = query.where(ShipmentOrderInfo.is_exception == f.isException)

        # query:未排序的Peewee查询对象(ModelSelect)
        return query

class OrderDetail:
    """出货订单详情"""
    def __init__(self, order_code: str):
        self.order_code = order_code

    def get_detail(self):
        """获取详情数据"""
        order = ShipmentOrderInfo.get(ShipmentOrderInfo.order_code == self.order_code)
        return schemas.ShipmentItem(**order.model_dump())