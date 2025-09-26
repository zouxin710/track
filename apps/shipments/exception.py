"""异常处置接口类"""
from datetime import datetime
from functools import cached_property

from peewee import JOIN

from apps.models import ShipmentOrderException, ShipmentOrderInfo, ShipmentExceptionHandle
from apps.shipments import schemas


class ExceptionList:
    """异常列表接口类"""

    def __init__(self, filters: schemas.ShipmentsExceptionsRequest):
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
        query = self.query.order_by(ShipmentOrderException.create_time.desc()).paginate(self.filters.pageNum, self.filters.pageSize)
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

            record = schemas.ShipmentsExceptionsItem(
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
            ShipmentOrderException.create_time.alias("exception_date"),
            ShipmentOrderException.status,
            ShipmentOrderException.update_time
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
            query = query.where(ShipmentOrderException.create_time.between(t1, t2))
        if f.status:
            # 查询满足状态列表的所有数据
            query = query.where(ShipmentOrderException.status.in_(f.status))
        # query:未排序的Peewee查询对象(ModelSelect)
        return query


class ExceptionsProcessing:
    """异常处置接口类"""

    def __init__(self, exception_id: int, item: schemas.ShipmentsExceptionsProcessingRequest):
        self.exception_id = exception_id
        self.item = item

    def processing(self):
        """异常处理操作"""
        # 去异常信息表拿异常信息
        query_result = ShipmentOrderException.get_by_id(self.exception_id)
        order_code = query_result.order_code
        # 添加异常操作记录表一条记录
        item = self.item.model_dump()
        item["exception_id"] = self.exception_id
        item["order_code"] = order_code
        item["operator_uid"] = 1
        item["operator_name"] = "admin"
        item["create_time"] = datetime.now()
        item["update_time"] = datetime.now()
        ShipmentExceptionHandle.create(**item)
        # 更新异常信息表的处置状态
        query_result.update(status=self.item.status, update_time=datetime.now()).where(ShipmentOrderException.id == self.exception_id).execute()


class ExceptionLogs:
    """异常日志列表接口类"""

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
            logs = []
        else:
            logs = self.get_details()
        # **pagination.model_dump() 将字典解包为关键字参数
        # ShipmentsOrdersResult返回内容列表content,分页信息
        return schemas.ShipmentsExceptionLogsResult(content=logs, **pagination.model_dump())

    def get_total(self) -> int:
        """拿取查询的结果总数"""
        return self.query.count()

    def get_details(self) -> list:
        """拿取查询的结果详情"""
        query = self.query.order_by(ShipmentExceptionHandle.create_time.desc()).paginate(self.filters.pageNum, self.filters.pageSize)
        records = []
        for q in query:
            # model_validate 用于验证和转换输入数据为 Pydantic模型实例
            exception = schemas.ExceptionLogsItem.model_validate(q)
            if hasattr(q, 'e'):
                exception_info = schemas.ExceptionLogsJoinExceptionItem.model_validate(q.e)
            else:
                # 默认值为None
                exception_info = schemas.ExceptionLogsJoinExceptionItem()
            if hasattr(q, 's'):
                order_info = schemas.ExceptionLogsJoinInfoItem.model_validate(q.s)
            else:
                # 默认值为None
                order_info = schemas.ExceptionLogsJoinInfoItem()

            record = schemas.ShipmentsExceptionLogsItem(
                **order_info.model_dump(),
                **exception.model_dump(),
                **exception_info.model_dump(),
            )
            records.append(record)
        return records

    @cached_property
    def query(self):
        """查询数据库操作"""
        # 从ShipmentExceptionHandle表中选择需要的字段
        # 并通过order_code关联ShipmentOrderInfo表获取额外字段
        query = (ShipmentExceptionHandle.select(
            # 处置记录表字段
            ShipmentExceptionHandle.id,
            ShipmentExceptionHandle.status,
            ShipmentExceptionHandle.content,
            ShipmentExceptionHandle.operator_name,
            # 异常信息表字段
            ShipmentOrderException.exception_type,
            ShipmentOrderException.exception_node,
            ShipmentOrderException.create_time,
            # 订单信息表字段
            ShipmentOrderInfo.first_leg_tracking_number,
            ShipmentOrderInfo.shipment_name
        ).join(
            ShipmentOrderInfo,
            on=(ShipmentExceptionHandle.order_code == ShipmentOrderInfo.order_code),
            join_type=JOIN.LEFT_OUTER,
            attr='s'
        )  # 三个表关联查询时 需要用switch切回主表
        .switch(ShipmentExceptionHandle)  # 切回主表
        .join(
            ShipmentOrderException,
            on=(ShipmentExceptionHandle.exception_id == ShipmentOrderException.id),
            join_type=JOIN.LEFT_OUTER,
            attr='e'
        ))

        f = self.filters
        # 字符串精确匹配条件
        if f.orderCode:
            query = query.where(ShipmentExceptionHandle.order_code == f.orderCode)
        if f.firstLegTrackingNumber:
            query = query.where(ShipmentOrderInfo.first_leg_tracking_number == f.firstLegTrackingNumber)
        if f.shipmentName:
            query = query.where(ShipmentOrderInfo.shipment_name == f.shipmentName)
        if f.exceptionId:
            query = query.where(ShipmentOrderException.id == f.exceptionId)
        # query:未排序的Peewee查询对象(ModelSelect)
        return query
