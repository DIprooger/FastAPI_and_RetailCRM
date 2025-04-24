import json
import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
import urllib.parse

from app.schemas.pay import PaymentAttachRequest

load_dotenv()

MY_CRM_NAME = os.getenv("MY_CRM_NAME")
BASE_URL = f"https://{MY_CRM_NAME}.retailcrm.ru/api/v5"
API_KEY_RETAILCRM = os.getenv("API_KEY_RETAILCRM")

async def get_customers(params: dict):
    params["apiKey"] = API_KEY_RETAILCRM
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/customers", params=params)
        response.raise_for_status()
        return response.json()

async def post_customers(customer_data: dict):
    customer_json_str = urllib.parse.quote_plus(str(customer_data).replace("'", '"'))
    payload = f"site={MY_CRM_NAME}&customer={customer_json_str}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = f"{BASE_URL}/customers/create?apiKey={API_KEY_RETAILCRM}"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload, headers=headers)
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()

async def get_order(customer_id):
    try:
        url = f"{BASE_URL}/orders"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "apiKey": API_KEY_RETAILCRM,
            "filter[customerId]	": customer_id,
        }
        encoded_payload = urllib.parse.urlencode(payload)

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}?{encoded_payload}", headers=headers)
            response.raise_for_status()
        return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Request failed: {exc}")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


async def post_order(order_data: dict) -> dict:
    try:
        order_json = json.dumps(order_data, ensure_ascii=False)
        order_encode = urllib.parse.quote_plus(order_json)

        payload = f"site={MY_CRM_NAME}&order={order_encode}"
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        url = f"{BASE_URL}/orders/create?apiKey={API_KEY_RETAILCRM}"

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload, headers=header)
            response.raise_for_status()
        return response.json()

    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Request failed: {exc}")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


async def post_pay(data: PaymentAttachRequest):
    payment_payload = {
        "amount": data.payment_amount,
        "order": data.payment_order.dict(),
        "type": data.payment_type,
        "status": data.payment_status,
    }

    form = {
        "apiKey": API_KEY_RETAILCRM,
        "site": data.site,
        "payment": json.dumps(payment_payload, ensure_ascii=False)
    }
    encoded = urllib.parse.urlencode(form)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/orders/payments/create?apiKey={API_KEY_RETAILCRM}",
            data=encoded,
            headers=headers
        )
        resp.raise_for_status()
        return resp.json()