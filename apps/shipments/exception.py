"""异常处置接口类"""
from functools import cached_property

from peewee import JOIN

from apps.models import ShipmentOrderException, ShipmentOrderInfo, ShipmentExceptionHandle
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
        return schemas.ShipmentsExceptionsResult(content=details, **pagination.model_dump())

    def get_total(self) -> int:
        """拿取查询的结果总数"""
        return self.query.count()

    def get_details(self) -> list:
        """拿取查询的结果详情"""
        query = self.query.order_by(ShipmentOrderException.exception_date.desc()).paginate(self.filters.pageNum, self.filters.pageSize)
        records = []
        for q in query:
            # model_validate 用于验证和转换输入数据为 Pydantic模型实例
            exception = schemas.ExceptionsItem.model_validate(q)
            # 订单头程号
            if hasattr(q, 't'):
                order_info = schemas.ExceptionsJoinItem.model_validate(q.t)
            else:
                # 默认值为None
                order_info = schemas.ExceptionsJoinItem()

            record = schemas.ShipmentExceptionsItem(
                **exception.model_dump(),
                **order_info.model_dump()
            )
            records.append(record)
        return records

    @cached_property
    def query(self):
        """查询数据库操作"""
        # 从ShipmentOrderException表中选择需要的字段
        # 并通过order_code关联ShipmentOrderInfo表获取额外字段
        query = ShipmentOrderException.select(
            ShipmentOrderException.id.alias('exception_id'),
            ShipmentOrderException.order_code,
            # 从关联表获取这三个字段
            ShipmentOrderInfo.provider_code,
            ShipmentOrderInfo.shipment_name,
            ShipmentOrderInfo.first_leg_tracking_number,
            ShipmentOrderException.exception_type,
            ShipmentOrderException.exception_node,
            ShipmentOrderException.exception_date
        ).join(
            ShipmentOrderInfo,
            # 通过order_code建立两个表的连接
            join_type=JOIN.LEFT_OUTER,
            on=(ShipmentOrderException.order_code == ShipmentOrderInfo.order_code),
            attr="t",
        )

        f = self.filters
        # 字符串精确匹配条件
        if f.orderCode:
            query = query.where(ShipmentOrderException.order_code == f.orderCode)
        if f.firstLegTrackingNumber:
            query = query.where(ShipmentOrderInfo.first_leg_tracking_number == f.firstLegTrackingNumber)
        if f.shipmentName:
            query = query.where(ShipmentOrderInfo.shipment_name == f.shipmentName)
        if f.exceptionType:
            query = query.where(ShipmentOrderException.exception_type == f.exceptionType)
        if f.exceptionNode:
            query = query.where(ShipmentOrderException.exception_node == f.exceptionNode)
        if f.exceptionDate and len(f.exceptionDate) == 2:
            # 时间范围
            t1, t2 = sorted(f.exceptionDate)
            query = query.where(ShipmentOrderException.exception_date.between(t1, t2))

        # query:未排序的Peewee查询对象(ModelSelect)
        return query


class ExceptionLogs:
    """异常日志接口类"""

    def __init__(self, filters: schemas.ShipmentsExceptionsLogsRequest):
        self.filters = filters

    def get_logs(self):
        """获取异常日志操作记录"""
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

    @cached_property
    def query(self):
        """查询数据库操作"""
        # 从ShipmentExceptionHandle表中选择需要的字段
        # 并通过order_code关联ShipmentOrderInfo表获取额外字段
        query = ShipmentExceptionHandle.select(
            ShipmentExceptionHandle.id,
            ShipmentExceptionHandle.shipment_name,
            ShipmentExceptionHandle.exception_type,
            ShipmentExceptionHandle.exception_node,
            ShipmentExceptionHandle.exception_date,
            ShipmentExceptionHandle.exception_status,
            ShipmentExceptionHandle.operator_name,
            ShipmentExceptionHandle.content,
            # 从关联表获取这个字段
            ShipmentOrderInfo.first_leg_tracking_number,
        ).join(
            ShipmentOrderInfo,
            # 通过order_code建立两个表的连接
            join_type=JOIN.LEFT_OUTER,
            on=(ShipmentExceptionHandle.order_code == ShipmentOrderInfo.order_code),
            attr="t",
        )

        f = self.filters
        # 字符串精确匹配条件
        if f.orderCode:
            query = query.where(ShipmentExceptionHandle.order_code == f.orderCode)
        ################################
        if f.firstLegTrackingNumber:
            query = query.where(ShipmentOrderInfo.first_leg_tracking_number == f.firstLegTrackingNumber)
        if f.shipmentName:
            query = query.where(ShipmentOrderInfo.shipment_name == f.shipmentName)

        # query:未排序的Peewee查询对象(ModelSelect)
        return query
