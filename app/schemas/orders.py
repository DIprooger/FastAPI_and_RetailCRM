from pydantic import BaseModel
from typing import Optional, List

class Customer(BaseModel):
    id: Optional[int] = None

class Item(BaseModel):
    productName: str
    initialPrice: float
    quantity: int = 1

class OrderRequest(BaseModel):
    number: str
    customer: Customer
    items: List[Item]
