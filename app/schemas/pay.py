from pydantic import BaseModel
from typing import Optional

class OrderReference(BaseModel):
    id: Optional[int] = None
    externalId: Optional[str] = None
    number: Optional[str] = None

class PaymentAttachRequest(BaseModel):
    site: str
    payment_amount: float
    payment_order: OrderReference
    payment_type: str
    payment_status: str
