"""
Custom exception classes for the AI Fitness Ecosystem.
All exceptions follow a consistent pattern for API error responses.
"""

from typing import Any, Optional


class AppException(Exception):
    """Base exception for the application."""
    def __init__(
        self,
        message: str = "An error occurred",
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Any] = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource", resource_id: Any = None):
        detail = f"{resource} not found"
        if resource_id:
            detail = f"{resource} with id '{resource_id}' not found"
        super().__init__(
            message=detail,
            code=f"{resource.upper().replace(' ', '_')}_NOT_FOUND",
            status_code=404,
        )


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, code="UNAUTHORIZED", status_code=401)


class ForbiddenException(AppException):
    def __init__(self, message: str = "You do not have permission to perform this action"):
        super().__init__(message=message, code="FORBIDDEN", status_code=403)


class ConflictException(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message=message, code="CONFLICT", status_code=409)


class ValidationException(AppException):
    def __init__(self, message: str = "Validation error", details: Any = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class RateLimitException(AppException):
    def __init__(self, message: str = "Rate limit exceeded. Please try again later."):
        super().__init__(message=message, code="RATE_LIMIT_EXCEEDED", status_code=429)


class ExternalServiceException(AppException):
    def __init__(self, service: str, message: str = "External service unavailable"):
        super().__init__(
            message=f"{service}: {message}",
            code="EXTERNAL_SERVICE_ERROR",
            status_code=502,
        )


class FileUploadException(AppException):
    def __init__(self, message: str = "File upload failed"):
        super().__init__(message=message, code="FILE_UPLOAD_ERROR", status_code=400)
