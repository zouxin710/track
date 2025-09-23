"""异常处置接口类"""
from functools import cached_property

from apps.models import ShipmentOrderException
from apps.shipments import schemas


class ExceptionList:
    """异常列表接口类"""
    def __init__(self, filters: schemas.ShipmentExceptionsRequest):
        # 初始化实例时 传入请求体filters
        self.filters = filters


    def get_list(self):
        """获取异常列表数据"""
        pagination = schemas.PaginationResponse(
            totalElements=self.get_total(),
            pageNum=self.filters.pageNum,
            pageSize=self.filters.pageSize,
        )

        # 拿列表
        # 判断 如果传入的页码数 > 总页数  则返回空列表
        if self.filters.pageNum > pagination.totalPages:
            details = []
        else:
            details = self.get_details()
        # **pagination.model_dump() 将字典解包为关键字参数
        # ShipmentsOrdersResult返回内容列表content,分页信息
        return schemas.ShipmentsOrdersResult(content=details, **pagination.model_dump())

    def get_total(self) -> int:
        """拿取查询的结果总数"""
        return self.query.count()

    def get_details(self) -> list:
        """拿取查询的结果详情"""
        query = self.query.order_by(ShipmentOrderException.create_time.desc()).paginate(self.filters.pageNum, self.filters.pageSize)
        records = []
        for q in query:
            # model_validate 用于验证和转换输入数据为 Pydantic模型实例
            #orderCode='GRKRMIwWfq' firstLegTrackingNumber='398snJcRZm' lastMileTrackingNumber='2rZqYjuus6' countryCode='Guyana' warehouseCode='KMK4uTBLeS' shipmentName='Lau Sai Wing' providerCode='jY1dIPHuou' shippingChannel='SrP07XRMWb' shippingMethod='b1bMyyHFpN' boxNum=607 shippingDate=datetime.datetime(2021, 2, 8, 20, 27, 22) departureDate=datetime.datetime(2024, 3, 9, 10, 58, 54) portArrivalDate=datetime.datetime(2025, 1, 17, 9, 37, 46) deliveryDate=datetime.datetime(2018, 6, 10, 0, 11, 28) signedDate=datetime.datetime(2010, 12, 8, 18, 20, 26) signedNum=687 shelvedTime=datetime.datetime(2007, 7, 17, 19, 32, 59) isException=687 createTime=datetime.datetime(2025, 6, 21, 22, 21, 8)
            order = schemas.ShipmentOrdersItem.model_validate(q)
            records.append(order)
        return records

    @cached_property
    def query(self):
        """查询数据库操作"""
        query = ShipmentOrderException.select(
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