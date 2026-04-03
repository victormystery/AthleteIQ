"""
Custom Exception Handlers
Define custom exceptions and handlers for the API
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Union
import logging

logger = logging.getLogger(__name__)


class CareerAPIException(Exception):
    """Base exception for Career API"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ModelLoadException(CareerAPIException):
    """Exception raised when ML model fails to load"""
    def __init__(self, message: str = "Failed to load ML model"):
        super().__init__(message, status_code=500)


class PredictionException(CareerAPIException):
    """Exception raised when prediction fails"""
    def __init__(self, message: str = "Failed to generate predictions"):
        super().__init__(message, status_code=500)


class ValidationException(CareerAPIException):
    """Exception raised for validation errors"""
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, status_code=400)


class DataNotFoundException(CareerAPIException):
    """Exception raised when requested data is not found"""
    def __init__(self, message: str = "Data not found"):
        super().__init__(message, status_code=404)


async def career_api_exception_handler(
    request: Request,
    exc: CareerAPIException
) -> JSONResponse:
    """
    Handle custom CareerAPIException
    """
    logger.error(f"CareerAPIException: {exc.message}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message,
            "type": exc.__class__.__name__,
            "path": str(request.url)
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Validation error: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation failed",
            "details": errors,
            "path": str(request.url)
        }
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Handle general exceptions
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": str(request.url)
        }
    )


def register_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI app
    """
    app.add_exception_handler(CareerAPIException, career_api_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
