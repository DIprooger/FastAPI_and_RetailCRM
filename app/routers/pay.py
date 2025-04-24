from fastapi import APIRouter
from app.schemas.pay import PaymentAttachRequest
from app.services.retailcrm_client import post_pay

pay_router = APIRouter()

@pay_router.post("/payments/create")
async def create_payment(payment: PaymentAttachRequest):
    return await post_pay(payment)
