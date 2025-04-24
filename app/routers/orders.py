from app.schemas.orders import OrderRequest
from fastapi import APIRouter, Query
from typing import Optional
from app.services.retailcrm_client import post_order, get_order

order_router = APIRouter()

@order_router.get("/orders")
async def list_order(customer_id: Optional[int] = Query(None, elies="customer id")):
    return await get_order(customer_id)

@order_router.post("/order/create")
async def create_order(order: OrderRequest):
    order_payload = {
        "number": order.number,
        "customer": order.customer.dict(exclude_unset=True),
        "items": [item.dict() for item in order.items],
    }

    response = await post_order(order_payload)
    return response