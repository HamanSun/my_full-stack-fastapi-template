import uuid

from datetime import datetime
from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)

# 订单名单
class OrderItem(SQLModel, table=True):
    __tablename__ = "orderitem"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, sa_column_kwargs={"comment": "主键"})
    order_id: uuid.UUID = Field(nullable=False, max_length=100, sa_column_kwargs={"comment": "订单号，对应order.id"}, foreign_key="order.id", ondelete="CASCADE")
    product_no: str = Field(nullable=False, max_length=100, sa_column_kwargs={"comment": "商品编号"})
    product_name: str | None = Field(default=None, max_length=255, sa_column_kwargs={"comment": "商品名称"})
    count: int = Field(default=1, ge=1, sa_column_kwargs={"comment": "购买数量"})
    unit_price: float = Field(default=0.0, ge=0.0, sa_column_kwargs={"comment": "商品单价"})
    order: Optional["Order"] = Relationship(back_populates="order_items")

# 订单
class Order(SQLModel, table=True):
    __tablename__ = "order"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, sa_column_kwargs={"comment": "主键"})
    order_no: str = Field(unique=True,index=True,max_length=100, sa_column_kwargs={"comment": "订单号"})
    total_amount: float =Field(default=0.0, ge=0.0, sa_column_kwargs={"comment": "总金额"})
    created_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"comment": "下单时间"})
    owner_id: uuid.UUID = Field(nullable=False,sa_column_kwargs={"comment": "下单人ID，对应user.id"})
    order_items: List[OrderItem] = Relationship(back_populates="order")

