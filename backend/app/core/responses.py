"""
Standardized API response wrappers.
Every endpoint returns {"success": bool, "data": ..., "message": str}.
"""

from typing import Any, Optional
from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
) -> dict:
    """Standard success response."""
    body: dict = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return body


def paginated_response(
    data: list,
    total: int,
    page: int,
    limit: int,
    message: str = "Success",
) -> dict:
    """Standard paginated response."""
    pages = (total + limit - 1) // limit if limit > 0 else 0
    return {
        "success": True,
        "message": message,
        "data": data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1,
        },
    }


def error_response(
    message: str = "An error occurred",
    code: str = "INTERNAL_ERROR",
    status_code: int = 500,
    details: Any = None,
) -> JSONResponse:
    """Standard error response as JSONResponse."""
    body: dict = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    if details is not None:
        body["error"]["details"] = details
    return JSONResponse(status_code=status_code, content=body)
