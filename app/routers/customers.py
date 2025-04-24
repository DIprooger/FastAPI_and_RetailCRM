from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.schemas.customers import CustomerCreateRequest
from app.services.retailcrm_client import get_customers, post_customers

customers_router = APIRouter()

@customers_router.get("/customers")
async def list_customers(
        name: Optional[str] = Query(None, elies="email"),
        email: Optional[str] = Query(None, alias="email"),
        created_at_from: Optional[str] = Query(None, alias="createdAtFrom")
):
    filters = {}
    if name:
        filters["filter[firstName]"] = name
    if email:
        filters["filter[email]"] = email
    if created_at_from:
        filters["filter[createdAtFrom]"] = created_at_from
    return await get_customers(filters)

@customers_router.post("/customer/create")
async def create_customer(request: CustomerCreateRequest):
    customer_dict = request.customer.dict()
    crm_response = await post_customers(customer_dict)
    return crm_response

