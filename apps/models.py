"""
数据库模型类
"""

from peewee import *

mysql_database = MySQLDatabase('jcs', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': 'localhost', 'user': 'root', 'password': '123456'})


# 定义一个基础模型类，继承自Model
class BaseModel(Model):
    """定义一个内部Meta类，用于配置模型的元数据"""
    class Meta:
        # 设置数据库连接，指向之前定义的database对象
        database = mysql_database

class ShipmentOrderInfo(BaseModel):
    """所有订单基本信息表/订单列表/订单明细"""
    order_code = CharField(unique=True)
    first_leg_tracking_number = CharField(index=True)
    last_mile_tracking_number = CharField(index=True, null=True)
    add_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    shipment_name = CharField()
    provider_code = CharField()
    shipping_warehouse = CharField(null=True)
    country_code = CharField(null=True)
    destination = CharField(null=True)
    warehouse_code = CharField()
    business_code = CharField(null=True)
    item_num = IntegerField(constraints=[SQL("DEFAULT 0")])
    shipping_channel = CharField(null=True)
    shipping_method = CharField(null=True)
    box_num = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    weight = DecimalField(null=True)
    volume_weight = DecimalField(null=True)
    billing_heavy = DecimalField(null=True)
    price = DecimalField(null=True)
    freight = DecimalField(null=True)
    total_cost = DecimalField(null=True)
    provider_cost = DecimalField(null=True)
    cost_difference = DecimalField(null=True)
    customs_duty = DecimalField(null=True)
    clearance_fee = DecimalField(null=True)
    extra_category_fee = DecimalField(null=True)
    super_product_fee = DecimalField(null=True)
    deduction = DecimalField(null=True)
    shipping_date = DateTimeField(null=True)
    departure_date = DateTimeField(null=True)
    port_arrival_date = DateTimeField(null=True)
    delivery_date = DateTimeField(null=True)
    shipping_status = CharField(constraints=[SQL("DEFAULT '待发货'")], null=True)
    signed_date = DateTimeField(null=True)
    signed_num = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    shelved_time = DateTimeField(null=True)
    total_track = TextField(null=True)
    tracking_history = TextField(null=True)
    latest_track_time = DateTimeField(null=True)
    remark = TextField(null=True)
    is_exception = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'shipment_order_info'

class ShipmentFirstLegTracking(BaseModel):
    """所有订单头程追踪表(记录ai提示词结果的表)"""
    order_code = CharField()
    node_id = CharField()
    track_time = DateTimeField(null=True)
    track_content = TextField()
    track_type = CharField(null=True)
    track_node = CharField(null=True)
    node_date = DateField(null=True)
    confidence = DecimalField(null=True)
    identify_status = CharField(constraints=[SQL("DEFAULT '自动采纳'")], null=True)
    artificial_review_time = DateTimeField(null=True)
    artificial_track_type = CharField(null=True)
    artificial_track_node = CharField(null=True)
    artificial_node_date = DateField(null=True)
    operator_uid = IntegerField(null=True)
    operator_name = CharField(null=True)
    source = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'shipment_first_leg_tracking'
        indexes = (
            (('order_code', 'node_id'), True),
        )
class ShipmentExceptionHandle(BaseModel):
    """订单异常处置记录表"""
    order_code = CharField(index=True)
    shipment_name = CharField(null=True)
    exception_type = CharField(null=True)
    exception_node = CharField(null=True)
    exception_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    exception_status = CharField(constraints=[SQL("DEFAULT '待处理'")], null=True)
    content = TextField(null=True)
    operator_uid = IntegerField(null=True)
    operator_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'shipment_exception_handle'

class ShipmentOrderException(BaseModel):
    """订单所有异常数据表"""
    order_code = CharField(index=True, null=True)
    exception_type = CharField(null=True)
    exception_node = CharField(null=True)
    exception_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    exception_status = CharField(constraints=[SQL("DEFAULT '待处理'")], null=True)
    exception_describe = TextField(null=True)
    status_change = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    operator_uid = IntegerField(null=True)
    operator_name = CharField(null=True)
    identify_time = DateTimeField(null=True)
    operate_content = TextField(null=True)

    class Meta:
        table_name = 'shipment_order_exception'

class ShipmentProviderTracking(BaseModel):
    """物流接口返回的原始信息记录表"""
    order_code = CharField()
    first_leg_tracking_number = CharField(null=True)
    first_leg_tracking = TextField()
    is_first_finished = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'shipment_provider_tracking'

