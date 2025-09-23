from flask import blueprints
from flask_pydantic import validate

from apps.shipments.schemas import *
from apps.shipments.order import OrderList, OrderDetail
from apps.shipments.track import ProviderTracking

order_bp = blueprints.Blueprint("order", __name__)
track_bp = blueprints.Blueprint("track", __name__)
exception_bp = blueprints.Blueprint("exception", __name__)

@order_bp.route("/orders", methods=["GET"])
@validate()
def orders(query: ShipmentsOrdersRequest):
    """获取订单列表的逻辑函数"""
    content = OrderList(filters=query).get_list()

    return Response(result=content)

@order_bp.route("/orders/<order_code>", methods=["GET"])
@validate()
def order_detail(order_code:str):
    """获取根据订单号获取订单详情的逻辑函数"""
    result = OrderDetail(order_code=order_code).get_detail()
    return Response(result=result)

@track_bp.route("/<order_code>/first-leg-tracking/provider-nodes", methods=["GET"])
@validate()
def track(order_code:str):
    """获取物流商原始头程原始轨迹"""
    result = ProviderTracking(order_code=order_code).get_tracking()
    return Response(result=result)


@exception_bp.route("/exceptions", methods=["GET"])
@validate()
def exception(query:ShipmentExceptionsRequest):
    """获取异常列表"""
    content = OrderList(filters=query).get_list()
    return Response(result=content)