from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import httpx

from exponential_core.exceptions.base import CustomAppException
from exponential_core.exceptions.handler import (
    http_exception_handler,
    validation_exception_handler,
    pydantic_validation_handler,
    httpx_error_handler,
    custom_app_exception_handler,
    general_exception_handler,
)
from exponential_core.logger.configure import configure_logging

logger = configure_logging()


class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            # Delegar a los handlers específicos si coincide el tipo
            if isinstance(exc, CustomAppException):
                return await custom_app_exception_handler(request, exc)
            elif isinstance(exc, RequestValidationError):
                return await validation_exception_handler(request, exc)
            elif isinstance(exc, ValidationError):
                return await pydantic_validation_handler(request, exc)
            elif isinstance(exc, httpx.RequestError):
                return await httpx_error_handler(request, exc)
            elif isinstance(exc, HTTPException):
                return await http_exception_handler(request, exc)
            else:
                # Fallback para cualquier error no controlado
                return await general_exception_handler(request, exc)
