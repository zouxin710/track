"""头程轨迹跟踪接口类"""

from apps.models import ShipmentFirstLegTracking
from apps.shipments import schemas


class ProviderTracking:
    """供应商原始轨迹"""
    def __init__(self, order_code: str,):
        self.order_code =  order_code

    def get_tracking(self):
        """获取供应商原始轨迹"""
        query = self.query().order_by(ShipmentFirstLegTracking.track_time.desc())
        # 存放节点的列表
        node_list = []
        for q in query:
            # q是一条查询结果 里面包含一个节点时间 一个节点内容
            # q 验证并转换为 ProviderTrackingItem 实例
            detail = schemas.ProviderTrackingItem.model_validate(q)
            node_list.append(detail)
        return schemas.ProviderTrackingResult(nodes=node_list)



    def query(self):
        """查询数据库操作"""
        query = ShipmentFirstLegTracking.select(
            ShipmentFirstLegTracking.track_time,
            ShipmentFirstLegTracking.track_content
        )
        query = query.where(ShipmentFirstLegTracking.order_code == self.order_code)
        print(query)
        return query