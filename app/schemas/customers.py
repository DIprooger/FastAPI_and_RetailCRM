from pydantic import BaseModel, EmailStr
from typing import List

class Phone(BaseModel):
    number: str

class CustomerData(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phones: List[Phone]

class CustomerCreateRequest(BaseModel):
    customer: CustomerData

