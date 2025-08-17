from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from sqlalchemy.exc import IntegrityError


class ExceptionHandlers:
    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": exc.errors(), "body": exc.body},
        )

    @staticmethod
    async def not_found_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"detail": "Resource not found"},
        )

    @staticmethod
    async def method_not_allowed_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=HTTP_405_METHOD_NOT_ALLOWED,
            content={"detail": "Method not allowed"},
        )

    @staticmethod
    async def conflict_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"detail": "Conflict: integrity violation"},
        )

    @staticmethod
    async def unprocessable_entity_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": str(exc.detail) if hasattr(exc, "detail") else "Invalid entity"},
        )

    @staticmethod
    async def internal_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )

    @classmethod
    def register(cls, app):
        app.add_exception_handler(RequestValidationError, cls.validation_exception_handler)
        app.add_exception_handler(StarletteHTTPException, cls.not_found_handler)
        app.add_exception_handler(StarletteHTTPException, cls.method_not_allowed_handler) 
        app.add_exception_handler(IntegrityError, cls.conflict_handler)      
        app.add_exception_handler(Exception, cls.internal_error_handler)         
