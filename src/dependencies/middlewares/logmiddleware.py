import time
import traceback
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from src.logs.logger import get_logger

logger = get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host
        method = request.method
        path = request.url.path

        try:
            response: Response = await call_next(request)
            status_code = response.status_code
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                "request_failed",
                extra={
                    "extra": {
                        "ip": client_ip,
                        "method": method,
                        "path": path,
                        "status": 500,
                        "duration": round(process_time, 3),
                        "error": str(e),
                        "traceback": traceback.format_exc(),
                    }
                },
            )
            raise e

        process_time = time.time() - start_time
        logger.info(
            "request_success",
            extra={
                "extra": {
                    "ip": client_ip,
                    "method": method,
                    "path": path,
                    "status": status_code,
                    "duration": round(process_time, 3),
                }
            },
        )
        return response
