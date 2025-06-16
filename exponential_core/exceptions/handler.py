import httpx
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError



logger = configure_logging()


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            str(exc.detail), "HTTPException", exc.status_code
        ),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"RequestValidationError en {request.url.path} | Detalle: {exc}")
    return JSONResponse(
        status_code=422,
        content=format_error_response(str(exc), "ValidationError", 422),
    )


async def pydantic_validation_handler(request: Request, exc: ValidationError):
    logger.warning(f"Pydantic ValidationError en {request.url.path} | Detalle: {exc}")
    return JSONResponse(
        status_code=422,
        content=format_error_response(str(exc), "PydanticValidation", 422),
    )


async def httpx_error_handler(request: Request, exc: httpx.RequestError):
    logger.error(f"Error de red con servicio externo en {request.url} | {repr(exc)}")
    return JSONResponse(
        status_code=502,
        content=format_error_response(
            "Error al comunicarse con servicio externo", "ExternalServiceError", 502
        ),
    )


async def custom_app_exception_handler(request: Request, exc: CustomAppException):
    logger.error(
        f"[{exc.__class__.__name__}] {exc.status_code} en {request.method} {request.url.path} | {exc.message} | Data: {exc.data}"
    )

    response = format_error_response(
        message=exc.message,
        error_type=exc.__class__.__name__,
        status_code=exc.status_code,
    )

    if exc.data:
        response["data"] = exc.data

    return JSONResponse(status_code=exc.status_code, content=response)


async def general_exception_handler(request: Request, exc: Exception):
    logger.critical(
        f"Excepción no controlada en {request.url.path} | {type(exc).__name__}",
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content=format_error_response(
            "Internal server error", "UnhandledException", 500
        ),
    )
