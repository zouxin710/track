from typing import Any, Optional, Type

from pydantic import BaseModel
from peewee import Model
class BaseModelWithORM(BaseModel):
    """基础模型, 用于继承, 包含ORM模型"""

    class Config:
        from_attributes = True
        populate_by_name = True

    def to_dict(self, alias_by=False, **kwargs) -> dict:
        return self.model_dump(by_alias=alias_by, **kwargs)

    def to_peewee(self, orm_model: Type[Model], by_alias=True, **kwargs) -> Model:
        fvs = self.model_dump(by_alias=by_alias, **kwargs)
        return orm_model(**fvs)