from flask import blueprints
from flask_pydantic import validate

from apps.shipments.schemas import *
from apps.shipments.order import OrderList

order_bp = blueprints.Blueprint("order", __name__)
track_bp = blueprints.Blueprint("track", __name__)

@order_bp.route("/orders", methods=["GET"])
@validate()
def orders(query: ShipmentsOrdersRequest):
    """获取订单列表的逻辑函数"""
    content = OrderList(filters=query).get_list()

    return Response(result=content)


@order_bp.route("/orders/<string:order_id>", methods=["GET"])
@validate()
def order_detail():
    """获取根据订单号获取订单详情的逻辑函数"""




    return Response()
@track_bp.route("/track", methods=["GET"])
@validate()
def track():
    return Response()
