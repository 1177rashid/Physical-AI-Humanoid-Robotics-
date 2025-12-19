from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Callable, Dict, Any
from enum import Enum
import traceback
import logging
from .logging import api_logger


class ErrorCode(Enum):
    # Authentication errors
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"

    # Resource errors
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"

    # Validation errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INPUT = "INVALID_INPUT"

    # System errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"

    # Business logic errors
    BUSINESS_RULE_VIOLATION = "BUSINESS_RULE_VIOLATION"


class CustomException(HTTPException):
    """Custom exception class for the application"""

    def __init__(self, error_code: ErrorCode, detail: str = None, status_code: int = None):
        self.error_code = error_code
        self.detail = detail or error_code.value
        self.status_code = status_code or self._get_default_status_code(error_code)

        super().__init__(status_code=self.status_code, detail=self.detail)

    def _get_default_status_code(self, error_code: ErrorCode) -> int:
        """Map error codes to HTTP status codes"""
        mapping = {
            ErrorCode.AUTHENTICATION_FAILED: status.HTTP_401_UNAUTHORIZED,
            ErrorCode.INSUFFICIENT_PERMISSIONS: status.HTTP_403_FORBIDDEN,
            ErrorCode.TOKEN_EXPIRED: status.HTTP_401_UNAUTHORIZED,
            ErrorCode.RESOURCE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
            ErrorCode.RESOURCE_ALREADY_EXISTS: status.HTTP_409_CONFLICT,
            ErrorCode.VALIDATION_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
            ErrorCode.INVALID_INPUT: status.HTTP_400_BAD_REQUEST,
            ErrorCode.BUSINESS_RULE_VIOLATION: status.HTTP_400_BAD_REQUEST,
            ErrorCode.INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
            ErrorCode.SERVICE_UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
        }
        return mapping.get(error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for the application"""

    # Log the exception
    api_logger.log_exception(f"Global exception handler caught: {str(exc)}")

    # Handle different types of exceptions
    if isinstance(exc, CustomException):
        error_response = {
            "error": {
                "code": exc.error_code.value,
                "message": exc.detail,
                "status_code": exc.status_code,
            }
        }
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )

    elif isinstance(exc, HTTPException):
        error_response = {
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "status_code": exc.status_code,
            }
        }
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response
        )

    else:
        # For unexpected errors
        error_response = {
            "error": {
                "code": ErrorCode.INTERNAL_ERROR.value,
                "message": "An internal server error occurred",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "details": str(exc) if __debug__ else None  # Don't expose error details in production
            }
        }
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response
        )


def add_exception_handlers(app):
    """Add exception handlers to the FastAPI application"""
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(HTTPException, global_exception_handler)
    app.add_exception_handler(CustomException, global_exception_handler)


def log_api_call(endpoint: str, method: str, status_code: int = None, execution_time: float = None):
    """Log API calls for monitoring and debugging"""
    api_logger.info(
        f"API Call: {method} {endpoint}",
        extra={
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "execution_time_ms": execution_time
        }
    )