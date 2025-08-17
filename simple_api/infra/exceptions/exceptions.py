from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.exc import IntegrityError
from simple_api.domain.exceptions.domain_exception import DomainException
from simple_api.core.logging import log

class ExceptionHandlers:
    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": exc.errors(), "body": exc.body},
        )

    @staticmethod
    async def starlette_http_handler(request: Request, exc: StarletteHTTPException):
        status_code = exc.status_code
        if status_code == HTTP_404_NOT_FOUND:
            detail = "Resource not found"
        elif status_code == HTTP_405_METHOD_NOT_ALLOWED:
            detail = "Method not allowed"
        else:
            detail = exc.detail if hasattr(exc, "detail") else "HTTP error"
        return JSONResponse(status_code=status_code, content={"detail": detail})

    @staticmethod
    async def conflict_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"detail": "Conflict: integrity violation"},
        )

    @staticmethod
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @staticmethod
    async def internal_error_handler(request: Request, exc: Exception):
        log.info(Exception)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )

    @classmethod
    def register(cls, app):
        app.add_exception_handler(RequestValidationError, cls.validation_exception_handler)
        app.add_exception_handler(StarletteHTTPException, cls.starlette_http_handler)
        app.add_exception_handler(IntegrityError, cls.conflict_handler)
        app.add_exception_handler(DomainException, cls.domain_exception_handler)
        app.add_exception_handler(Exception, cls.internal_error_handler)
