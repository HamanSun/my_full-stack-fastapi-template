import traceback
import uuid

from typing import Any, List

from fastapi import APIRouter, HTTPException, Body
from sqlalchemy import orm
from sqlalchemy.orm import joinedload
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.schemas.schemes import CreateOrderRequest, OrderListResponse, OrderResponse, OrderItemResponse
from app.models import Order, OrderItem


router = APIRouter(prefix="/order", tags=["order"])

@router.post("/buy", response_model=str)
async def create_order(session: SessionDep, user: CurrentUser, request: CreateOrderRequest = Body(...)) -> Any:
    # 先从request中获取商品列表中的商品数量及单价，计算总价
    total_amount = 0
    for item in request.items:
        total_amount += item.count * item.unit_price
    # 新建订单
    new_order = Order(
        order_no="ORDER_" + uuid.uuid4().hex,
        owner_id=user.id,
        total_amount=total_amount
    )
    # 根据入参，初始化订单的商品列表
    new_order_items = []
    for item in request.items:
        new_order_items.append(OrderItem(
            order_id=new_order.id,
            product_no=item.product_no,
            product_name=item.product_name,
            count=item.count,
            unit_price=item.unit_price
        ))
    # 事务操作：保存订单及订单商品
    try:
        session.add(new_order)
        session.add_all(new_order_items)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="下单失败，请稍后再试！" + str(e))
    return "下单成功！订单号：" + new_order.order_no

# 获取用户的所有订单，按创建时间倒序排列，支持分页, 返回总量及当前页数据列表
@router.get("/list", response_model=OrderListResponse)
async def get_user_orders(session: SessionDep, user: CurrentUser, skip: int = 0, limit: int = 10) -> Any:
    count_statement = select(func.count(Order.id)).where(Order.owner_id == user.id)
    total = session.exec(count_statement).one()
    order_page_data_statement = select(Order).where(Order.owner_id == user.id).order_by(Order.created_at.desc()).offset(skip).limit(limit)
    orders = session.exec(order_page_data_statement).all()
    return OrderListResponse(orders=orders, count=total)

# 获取用户所有订单，订单中要附加商品信息，按创建时间倒序排列，支持分页, 返回总量及当前页数据列表
@router.get("/list/with-items", response_model=OrderListResponse)
async def get_user_orders_with_items(session: SessionDep, user: CurrentUser, skip: int = 0, limit: int = 10) -> Any:
    count_statement = select(func.count(Order.id)).where(Order.owner_id == user.id)
    total = session.exec(count_statement).one()
    # 订单表
    order_page_data_statement = select(Order).where(Order.owner_id == user.id).order_by(Order.created_at.desc()).offset(skip).limit(limit)
    # 执行查询，获取订单
    try:
        # ========== 第一步：仅查订单表，按订单数精准分页 ==========
        # 1.1 查询分页后的订单（仅订单表，无 JOIN，保证分页准确性）
        order_stmt = (
            select(Order)
            .where(Order.owner_id == user.id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        # 执行查询，获取分页后的订单实例列表（比如 limit=10 就返回 10 个订单）
        paginated_orders = session.exec(order_stmt).all()
        if not paginated_orders:
            return OrderListResponse(orders=[], count=0)

        # 1.2 提取分页后的订单 ID 列表（用于批量查订单项）
        order_ids = [order.id for order in paginated_orders]

        # ========== 第二步：批量查询这些订单的所有订单项 ==========
        # 2.1 按订单 ID 批量查订单项（IN 查询，高效）
        item_stmt = select(OrderItem).where(OrderItem.order_id.in_(order_ids))
        order_items = session.exec(item_stmt).all()

        # 2.2 构建「订单 ID → 订单项列表」的映射（方便关联）
        item_map = {}
        for item in order_items:
            if item.order_id not in item_map:
                item_map[item.order_id] = []
            # 转换订单项为响应模型
            item_map[item.order_id].append(OrderItemResponse(
                id=item.id,
                order_id=item.order_id,
                product_no=item.product_no,
                product_name=item.product_name,
                count=item.count,
                unit_price=item.unit_price
            ))

        # ========== 第三步：关联订单项到对应订单 ==========
        order_responses = []
        for order in paginated_orders:
            # 构造订单响应模型，关联订单项（无订单项则为空列表）
            order_responses.append(OrderResponse(
                id=order.id,
                order_no=order.order_no,
                total_amount=order.total_amount,
                created_at=order.created_at,
                owner_id=order.owner_id,
                order_items=item_map.get(order.id, [])  # 关联订单项
            ))
        return OrderListResponse(orders=order_responses, count=total if total else 0)
    except Exception as e:
        traceback.print_exc()  # 打印堆栈信息，便于调试
        raise HTTPException(status_code=500, detail="获取订单列表失败，请稍后再试！" + str(e))

# 获取用户所有订单，订单中要附加商品信息，按创建时间倒序排列，支持分页, 返回总量及当前页数据列表
@router.get("/list/with-items2", response_model=OrderListResponse)
def get_user_orders(session: SessionDep, user: CurrentUser, skip: int = 0, limit: int = 10):
    try:
        # 关键1：使用 SQLModel 的 select + joinedload（导入路径不同）
        from sqlalchemy.orm import joinedload  # SQLModel 底层仍依赖 SQLAlchemy 的 joinedload

        # 步骤1：构造查询（预加载 order_items，避免懒加载）
        order_stmt = (
            select(Order)
            .where(Order.owner_id == user.id)
            .options(joinedload(Order.order_items))  # 预加载订单项，自动填充到 order_items
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        # 步骤2：执行查询（SQLModel 中用 session.exec() + unique() 去重）
        # 注意：SQLModel 的 session.exec() 等价于 SQLAlchemy 的 session.scalars()
        orders = session.exec(order_stmt).unique().all()

        # 步骤3：查询订单总数（单独查，避免 JOIN 干扰计数）
        total_stmt = select(func.count(Order.id)).where(Order.owner_id == user.id)
        total = session.exec(total_stmt).one()  # SQLModel 中用 one() 获取单个值

        # 此时 orders 中的每个 order.order_items 已正常加载订单项
        return OrderListResponse(orders=orders, count=total)

    except Exception as e:
        session.rollback()
        raise Exception(f"查询订单失败：{str(e)}")


@router.get("/list/with-items3", response_model=OrderListResponse)
def get_user_orders3(session: SessionDep, user: CurrentUser, skip: int = 0, limit: int = 10):
    try:
        # 关键：禁用子查询分页（解决映射失效）
        orm.configure_mappers()
        query = (
            session.query(Order)
            .options(joinedload(Order.order_items))  # 预加载订单项
            .filter(Order.owner_id == user.id)
            .order_by(Order.created_at.desc())
            .limit(limit)
            .offset(skip)
            .with_polymorphic('*')  # 兼容 SQLModel 多态查询
        )
        # 执行查询并去重（JOIN 导致的重复订单）
        orders = query.distinct().all()

        # 手动触发关联数据加载（强制填充 order_items）
        for order in orders:
            # 访问 order_items 触发懒加载（确保数据被加载）
            _ = order.order_items

        # 转换为响应模型（避免 422 错误）
        order_responses = []
        for order in orders:
            order_responses.append({
                "id": order.id,
                "order_no": order.order_no,
                "total_amount": order.total_amount,
                "created_at": order.created_at,
                "owner_id": order.owner_id,
                "order_items": [
                    {
                        "id": item.id,
                        "order_id": item.order_id,
                        "product_no": item.product_no,
                        "product_name": item.product_name,
                        "count": item.count,
                        "unit_price": item.unit_price
                    } for item in order.order_items
                ]
            })

        total = session.query(func.count(Order.id)).filter(Order.owner_id == user.id).scalar()
        return OrderListResponse(orders=order_responses, count=total)

    except Exception as e:
        session.rollback()
        raise Exception(f"查询订单失败：{str(e)}")

@router.get("/list/with-items4", response_model=OrderListResponse)
def get_user_orders(session: SessionDep, user: CurrentUser, skip: int = 0, limit: int = 10):
    try:
        # 1. 直接 JOIN 订单和订单项（无嵌套子查询）
        raw_stmt = (
            select(Order, OrderItem)
            .join(OrderItem, Order.id == OrderItem.order_id, isouter=True)  # LEFT JOIN
            .where(Order.owner_id == user.id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        # 执行查询，获取 (Order, OrderItem) 元组列表
        results = session.exec(raw_stmt).all()

        # 2. 手动重组数据（核心：将同一订单的订单项聚合）
        order_dict = {}
        for order, item in results:
            if order.id not in order_dict:
                # 初始化订单，手动创建 order_items 列表
                order_dict[order.id] = {
                    "id": order.id,
                    "order_no": order.order_no,
                    "total_amount": order.total_amount,
                    "created_at": order.created_at,
                    "owner_id": order.owner_id,
                    "order_items": []
                }
            # 仅当订单项非空时添加（排除 LEFT JOIN 带来的 NULL）
            if item is not None:
                order_dict[order.id]["order_items"].append({
                    "id": item.id,
                    "order_id": item.order_id,
                    "product_no": item.product_no,
                    "product_name": item.product_name,
                    "count": item.count,
                    "unit_price": item.unit_price
                })

        # 3. 转换为响应模型（适配 422 校验）
        orders = list(order_dict.values())
        total = session.exec(select(func.count(Order.id)).where(Order.owner_id == user.id)).one()

        # 4. 构造响应（确保与 OrderListResponse 字段匹配）
        return OrderListResponse(orders=orders, count=total)

    except Exception as e:
        session.rollback()
        raise Exception(f"查询订单失败：{str(e)}")