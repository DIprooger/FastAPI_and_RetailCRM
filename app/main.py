from fastapi import FastAPI
from app.routers.customers import customers_router
from app.routers.orders import order_router
from app.routers.pay import pay_router

app = FastAPI()

app.include_router(customers_router)
app.include_router(order_router)
app.include_router(pay_router)