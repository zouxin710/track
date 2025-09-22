from flask import blueprints
from flask_pydantic import validate

from apps.shipments.schemas import *
from apps.shipments.order import OrderList

order_bp = blueprints.Blueprint("order", __name__)
track_bp = blueprints.Blueprint("track", __name__)

@order_bp.route("/orders", methods=["GET"])
@validate()
def orders(query: ShipmentsOrdersRequest):
    pageSize = query.pageSize
    pageNum = query.pageNum

    content = OrderList(uid=315, filters=query).get_list()
    print(pageSize, pageNum)

    return ShipmentsOrdersResponse(result=content)

@track_bp.route("/track", methods=["GET"])
@validate()
def track():
    return Response()
