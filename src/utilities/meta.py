
from fastapi import Request

def get_ipaddr(request: Request):
    x_forwarded_for = request.headers.get("x-forwarded-for")
    return x_forwarded_for.split(",")[0].strip() if x_forwarded_for else request.client.host
