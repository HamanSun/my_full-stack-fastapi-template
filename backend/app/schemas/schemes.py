from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from app.models import Order, OrderItem

from datetime import datetime

# 订单基本信息
class OrderBase(BaseModel):
    id: str = Field(default=None, max_length=100, description="订单ID")
    order_no: str = Field(default=None, max_length=100, description="订单号")
    total_amount: float = Field(default=0.0, ge=0.0, description="订单总金额")
    created_at: datetime = Field(default=None, description="订单创建时间")
    owner_id: str = Field(default=None, max_length=100, description="订单所属用户ID")

# 下单商品信息
class OrderItemDto(BaseModel):
    product_no: str = Field(nullable=False, max_length=100)
    product_name: str | None = Field(default=None, max_length=255)
    count: int = Field(default=1, ge=1, description="商品数量必须大于0")
    unit_price: float = Field(default=0.0, ge=0.0, description="商品单价必须大于等于0")

# 创建订单请求
class CreateOrderRequest(BaseModel):
    # 订单项列表：非空 + 至少1项 + product_no不重复
    items: List[OrderItemDto] = Field(not_none=True, min_items=1)
    # 核心：验证 items 中 product_no 不重复

    @field_validator("items")
    def validate_items(cls, v):
        product_no_set = set()
        for item in v:
            if item.product_no in product_no_set:
                raise ValueError(f"product_no {item.product_no} 重复")
            product_no_set.add(item.product_no)
        return v

# 订单中包含的商品信息
class OrderItemResponse(BaseModel):
    order_id: str
    product_no: str
    product_name: str
    count: int
    unit_price: float


# 订单列表
class OrderListResponse(BaseModel):
    orders: List[Order]
    count: int

# 订单项响应模型（仅包含需要返回的字段）
class OrderItemResponse(BaseModel):
    id: Optional[UUID] = None
    order_id: Optional[UUID] = None
    product_no: Optional[str] = None
    product_name: Optional[str] = None
    count: Optional[int] = None
    unit_price: Optional[float] = None

# 订单响应模型（包含 order_items 列表）
class OrderResponse(BaseModel):
    id: UUID
    order_no: str
    total_amount: float
    created_at: datetime
    owner_id: UUID
    order_items: List[OrderItemResponse] = []  # 默认空列表

# 最终响应模型
class OrderListResponse(BaseModel):
    orders: List[OrderResponse]
    count: int