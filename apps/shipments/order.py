"""出货单管理接口类"""
from datetime import datetime
from functools import cached_property

from flask_pydantic import ValidationError

from apps.models import ShipmentOrderInfo
from apps.shipments import schemas


class OrderList:
    """出货订单列表"""

    def __init__(self, filters: schemas.ShipmentsOrdersRequest):
        # 初始化实例时 传入请求体filters
        self.filters = filters

    def get_list(self):
        """获取列表数据"""
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
        query = self.query.order_by(ShipmentOrderInfo.create_time.desc()).paginate(self.filters.pageNum, self.filters.pageSize)
        records = []
        for q in query:
            # model_validate 用于验证和转换输入数据为 Pydantic模型实例
            # orderCode='GRKRMIwWfq' firstLegTrackingNumber='398snJcRZm' lastMileTrackingNumber='2rZqYjuus6' countryCode='Guyana' warehouseCode='KMK4uTBLeS' shipmentName='Lau Sai Wing' providerCode='jY1dIPHuou' shippingChannel='SrP07XRMWb' shippingMethod='b1bMyyHFpN' boxNum=607 shippingDate=datetime.datetime(2021, 2, 8, 20, 27, 22) departureDate=datetime.datetime(2024, 3, 9, 10, 58, 54) portArrivalDate=datetime.datetime(2025, 1, 17, 9, 37, 46) deliveryDate=datetime.datetime(2018, 6, 10, 0, 11, 28) signedDate=datetime.datetime(2010, 12, 8, 18, 20, 26) signedNum=687 shelvedTime=datetime.datetime(2007, 7, 17, 19, 32, 59) isException=687 createTime=datetime.datetime(2025, 6, 21, 22, 21, 8)
            order = schemas.ShipmentsOrdersItem.model_validate(q)
            records.append(order)
        return records

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
            ShipmentOrderInfo.shipping_status,
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
            query = query.where(ShipmentOrderInfo.order_code.contains(f.orderCode))
        if f.firstLegTrackingNumber:
            query = query.where(ShipmentOrderInfo.first_leg_tracking_number.contains(f.firstLegTrackingNumber))
        if f.lastMileTrackingNumber:
            query = query.where(ShipmentOrderInfo.last_mile_tracking_number.contains(f.lastMileTrackingNumber))
        if f.shipmentName:
            query = query.where(ShipmentOrderInfo.shipment_name == f.shipmentName)
        if f.providerCode:
            query = query.where(ShipmentOrderInfo.provider_code == f.providerCode)
        if f.shippingMethod:
            query = query.where(ShipmentOrderInfo.shipping_method == f.shippingMethod)
        if f.shippingStatus:
            query = query.where(ShipmentOrderInfo.shipping_status == f.shippingStatus)
        if f.countryCode:
            query = query.where(ShipmentOrderInfo.country_code == f.countryCode)
        if f.warehouseCode:
            query = query.where(ShipmentOrderInfo.warehouse_code == f.warehouseCode)

        # 时间数组区间判断
        if f.shippingDate and len(f.shippingDate) == 2:
            # 发货时间范围
            t1, t2 = sorted(f.shippingDate)
            query = query.where(ShipmentOrderInfo.shipping_date.between(t1, t2))

        if f.departureDate and len(f.departureDate) == 2:
            # 开船时间范围
            t1, t2 = sorted(f.departureDate)
            query = query.where(ShipmentOrderInfo.departure_date.between(t1, t2))

        if f.portArrivalDate and len(f.portArrivalDate) == 2:
            # 到港时间范围
            t1, t2 = sorted(f.portArrivalDate)
            query = query.where(ShipmentOrderInfo.port_arrival_date.between(t1, t2))

        if f.deliveryDate and len(f.deliveryDate) == 2:
            # 派送时间范围
            t1, t2 = sorted(f.deliveryDate)
            query = query.where(ShipmentOrderInfo.delivery_date.between(t1, t2))

        if f.signedDate and len(f.signedDate) == 2:
            # 签收时间范围
            t1, t2 = sorted(f.signedDate)
            query = query.where(ShipmentOrderInfo.signed_date.between(t1, t2))

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
        try:
            # 执行查询获取数据
            query_result = self.query.get()

            # 将查询结果转换为 Pydantic 模型
            detail = schemas.ShipmentsDetailItem.model_validate(
                query_result,
            )

            return schemas.ShipmentsDetailItem(**detail.model_dump())
        # """    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  """
        except ShipmentOrderInfo.DoesNotExist:
            # 处理订单不存在的情况
            return {
                "error": "Order not found",
                "message": f"No order found with code: {self.order_code}"
            }, 404

        except ValidationError as e:
            # 处理数据验证错误
            return {
                "error": "Data validation error",
                "details": e.errors()
            }, 400

        except Exception as e:
            # 处理其他错误
            return {
                "error": "Internal server error",
                "message": str(e)
            }, 500

    @cached_property
    def query(self):
        """查询数据库操作"""
        # 创建查询对象 从数据库中选择ShipmentOrderInfo表中的所有记录
        query = ShipmentOrderInfo.select(
            ShipmentOrderInfo.order_code,
            ShipmentOrderInfo.first_leg_tracking_number,
            ShipmentOrderInfo.last_mile_tracking_number,
            ShipmentOrderInfo.warehouse_code,
            ShipmentOrderInfo.shipment_name,
            ShipmentOrderInfo.shipment_name,
            ShipmentOrderInfo.warehouse_code,
            ShipmentOrderInfo.add_time,
            ShipmentOrderInfo.provider_code,
            ShipmentOrderInfo.box_num,
            ShipmentOrderInfo.shipping_channel,
            ShipmentOrderInfo.shipping_method,
            ShipmentOrderInfo.country_code,
            ShipmentOrderInfo.weight,
            ShipmentOrderInfo.volume_weight,
            ShipmentOrderInfo.billing_heavy,
            ShipmentOrderInfo.price,
            ShipmentOrderInfo.freight,
            ShipmentOrderInfo.total_cost,
            ShipmentOrderInfo.provider_cost,
            ShipmentOrderInfo.customs_duty,
            ShipmentOrderInfo.clearance_fee,
            ShipmentOrderInfo.extra_category_fee,
            ShipmentOrderInfo.super_product_fee,
            ShipmentOrderInfo.deduction,
            ShipmentOrderInfo.cost_difference,
            ShipmentOrderInfo.shipping_status,
            ShipmentOrderInfo.shipping_date,
            ShipmentOrderInfo.departure_date,
            ShipmentOrderInfo.port_arrival_date,
            ShipmentOrderInfo.delivery_date,
            ShipmentOrderInfo.signed_date,
            ShipmentOrderInfo.shelved_time,
            ShipmentOrderInfo.signed_num,
            # ShipmentOrderInfo.total_tracking_number,
            # ShipmentOrderInfo.shipping_days,
            # ShipmentOrderInfo.warehouse_aging,
            # ShipmentOrderInfo.navigation_aging,
            # ShipmentOrderInfo.port_delivery_date,
            # ShipmentOrderInfo.delivery_accept_aging,
            # ShipmentOrderInfo.shelf_aging,
            ShipmentOrderInfo.remark,
            ShipmentOrderInfo.is_exception

        )
        query = query.where(ShipmentOrderInfo.order_code == self.order_code)
        # print(query.get().order_code) # 获取查询结果的第一条记录的order_code
        return query


class OrderModify:
    """出货订单修改"""

    def __init__(self, order_code: str, item: schemas.ShipmentsOrderUpdateRequest):
        self.order_code = order_code
        self.item = item

    def modify(self):
        """修改订单数据"""
        # peewee方法 若找不到记录返回None
        r = ShipmentOrderInfo.get_or_none(order_code=self.order_code)
        # 异常处理
        if not r:
            raise Exception("Order not found")

        # Pydantic 模型转换为字典 by_alias=True 确保使用字段别名
        item = self.item.model_dump(by_alias=True)
        item["update_time"] = datetime.now()
        # 执行更新
        ShipmentOrderInfo.update(**item).where(ShipmentOrderInfo.order_code == self.order_code).execute()
