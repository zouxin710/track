"""头程轨迹跟踪接口类"""
from functools import cached_property

from peewee import JOIN, fn

from apps.models import ShipmentFirstLegTracking, ShipmentOrderInfo
from apps.shipments import schemas


class TrackingNodes:
    """当前订单号下的所有轨迹节点"""

    def __init__(self, order_code: str, filters: schemas.ShipmentTrackingRequest):
        self.order_code = order_code
        self.filters = filters

    def get_tracking(self):
        """获取当下订单的所有轨迹节点"""
        query = self.query.order_by(ShipmentFirstLegTracking.track_time.desc())
        # 存放节点的列表
        node_list = []
        for q in query:
            # q是一条查询结果 里面包含一个节点时间 一个节点内容
            # q 验证并转换为 ProviderTrackingItem 实例
            detail = schemas.ShipmentsTrackingItem.model_validate(q)
            node_list.append(detail)
        return schemas.ShipmentsTrackingResult(nodeCount=self.get_count(), nodes=node_list)

    def get_count(self):
        """获取当下订单的节点数量"""
        return self.query.count()

    @cached_property
    def query(self):
        """查询数据库操作"""
        query = ShipmentFirstLegTracking.select(
            ShipmentFirstLegTracking.id,
            ShipmentFirstLegTracking.track_time,
            ShipmentFirstLegTracking.track_content,
            ShipmentFirstLegTracking.track_type,
            ShipmentFirstLegTracking.track_node,
            ShipmentFirstLegTracking.node_date,
            ShipmentFirstLegTracking.confidence,
            ShipmentFirstLegTracking.identify_status,
            ShipmentFirstLegTracking.artificial_review_time,
            ShipmentFirstLegTracking.artificial_track_type,
            ShipmentFirstLegTracking.artificial_track_node,
            ShipmentFirstLegTracking.artificial_node_date,
            ShipmentFirstLegTracking.source,
        )
        query = query.where(ShipmentFirstLegTracking.order_code == self.order_code)

        if self.filters.identifyStatus:
            query = query.where(ShipmentFirstLegTracking.identify_status == self.filters.identifyStatus)
        return query


class PendingList:
    """待审核轨迹订单列表"""

    def __init__(self, filters: schemas.ShipmentsPendingRequest):
        self.filters = filters

    def get_list(self):
        """获取待审核轨迹订单列表"""
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
        return schemas.ShipmentsPendingResult(content=details, **pagination.model_dump())

    def get_total(self):
        """获取待审核轨迹订单总数"""
        return self.query.count()

    def get_details(self):
        """获取查询结果存入列表"""
        query = self.query.paginate(self.filters.pageNum, self.filters.pageSize)
        # 存放带审核订单的列表
        pending_list = []
        for q in query:
            # q是一条查询结果 里面包含一个节点时间 一个节点内容
            # q 验证并转换为 ProviderTrackingItem 实例
            detail = schemas.ShipmentsPendingItem.model_validate(q)
            pending_list.append(detail)
        return pending_list

    @cached_property
    def query(self):
        """查询数据库操作"""
        query = (ShipmentOrderInfo.select(
            ShipmentOrderInfo.order_code,
            ShipmentOrderInfo.shipment_name,
            ShipmentOrderInfo.first_leg_tracking_number,
            ShipmentOrderInfo.last_mile_tracking_number,
            ShipmentOrderInfo.provider_code,
            ShipmentOrderInfo.shipping_channel,
            ShipmentOrderInfo.latest_track_time,
            # 统计每个订单对应的追踪记录数（重复次数）
            # fn是用于访问数据库函数的一个对象
            # 通过它可以调用像 COUNT、SUM、AVG、MAX、MIN 等各种数据库原生支持的聚合函数或者其他函数，来实现更复杂的查询操作
            fn.COUNT(ShipmentOrderInfo.order_code).alias('pending_count')
        ).group_by(ShipmentOrderInfo.order_code)
                 .join(ShipmentFirstLegTracking,
                       on=(ShipmentOrderInfo.order_code == ShipmentFirstLegTracking.order_code),
                       join_type=JOIN.INNER)
                 .where(ShipmentFirstLegTracking.identify_status == '待审核'))

        f = self.filters
        if f.orderCode:
            query = query.where(ShipmentOrderInfo.order_code.contains(f.orderCode))
        if f.shipmentName:
            query = query.where(ShipmentOrderInfo.shipment_name == f.shipmentName)
        if f.providerCode:
            query = query.where(ShipmentOrderInfo.provider_code == f.providerCode)

        return query
