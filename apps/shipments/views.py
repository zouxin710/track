from flask import blueprints
from flask_pydantic import validate

from apps.shipments.exception import ExceptionList, ExceptionLogs, ExceptionsProcessing
from apps.shipments.order import OrderList, OrderDetail, OrderModify
from apps.shipments.schemas import *
from apps.shipments.track import TrackingNodes, PendingList, TrackReview, AddNode

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
def order_detail(order_code: str):
    """获取根据订单号获取订单详情的逻辑函数"""
    result = OrderDetail(order_code=order_code).get_detail()
    return Response(result=result)


@order_bp.route("/orders/<orderCode>}/modify", methods=["PUT"])
@validate()
def order_modify(order_code: str, body: ShipmentsOrderUpdateRequest):
    """修改订单信息"""
    OrderModify(order_code=order_code, item=body).modify()
    return Response()


@track_bp.route("/<order_code>/first-leg-tracking/nodes", methods=["GET"])
@validate()
def nodes(order_code: str, query: ShipmentsTrackingRequest):
    """根据订单号获取所有轨迹节点列表"""
    result = TrackingNodes(order_code=order_code, filters=query).get_tracking()
    return Response(result=result)


@track_bp.route("/first-leg-tracking/orders", methods=["GET"])
@validate()
def pending(query: ShipmentsPendingRequest):
    """获取待审核订单列表"""
    content = PendingList(filters=query).get_list()
    return Response(result=content)


@track_bp.route("/first-leg-tracking/{id}/review", methods=["POST"])
@validate()
def review(id: int, body: ShipmentsReviewPostRequest):
    """人工审核提交"""
    TrackReview(id=id, item=body).submit()
    return Response()


@track_bp.route("/first-leg-tracking/add", methods=["POST"])
@validate()
def add_node(body: ShipmentsAddNodeRequest):
    """添加节点轨迹"""
    AddNode(item=body).add()
    return Response()


@exception_bp.route("/exceptions", methods=["GET"])
@validate()
def exception(query: ShipmentsExceptionsRequest):
    """获取异常列表"""
    content = ExceptionList(filters=query).get_list()
    return Response(result=content)


@exception_bp.route("/exceptions/{exception_id}/processing", methods=["POST"])
@validate()
def exception_processing(exception_id: int, body: ShipmentsExceptionsProcessingRequest):
    """异常操作"""
    ExceptionsProcessing(exception_id=exception_id, item=body).processing()
    return Response()


@exception_bp.route("/exceptions/logs", methods=["GET"])
@validate()
def exception_logs(query: ShipmentsExceptionsLogsRequest):
    """获取异常日志列表"""
    content = ExceptionLogs(filters=query).get_logs()
    return Response(result=content)
