from ninja import NinjaAPI
from post.api_v1 import router as post_api_v1
from post.authentication import APIAuthBearer
from django.http import HttpResponse
from functools import wraps
from ninja.errors import ValidationError, HttpError
from ninja.responses import Response
from django.http import Http404
import logging

# Initialize loggers
error_logger = logging.getLogger("api.error")

api = NinjaAPI(title="Blog API", version="1.0.0")
api.add_router("/v1", post_api_v1)

# Uncomment to enable API authentication
# api.add_router("/v1", post_api_v1, auth=APIAuthBearer())


@api.exception_handler(ValidationError)
def validation_exception_handler(request, exc):
    err_msg = "Validation error"
    errors = exc.errors
    if errors:
        first_error = errors[0]
        field = first_error.get("loc")[-1]
        msg = first_error.get("msg", "Unknown error")
        err_msg = f"Error in {field}: {msg}"

    # Log validation errors with error level
    error_logger.error(
        {
            "message": err_msg,
            "path": request.path,
            "method": request.method,
            "error_type": "ValidationError",
            "status_code": 422,
        }
    )
    return Response({"error": err_msg}, status=422)


@api.exception_handler(Http404)
def not_found_exception_handler(request, exc):
    error = str(exc)
    # Log not found errors
    error_logger.error(
        {
            "message": error,
            "path": request.path,
            "method": request.method,
            "error_type": "NotFoundError",
            "status_code": 404,
        }
    )
    return Response({"error": error}, status=404)


@api.exception_handler(Exception)
def global_exception_handler(request, exc: Exception):
    # Log unhandled errors
    error_logger.error(
        {
            "path": request.path,
            "method": request.method,
            "error_type": exc.__class__.__name__,
            "message": str(exc),
            "status_code": 500,
        }
    )
    return Response({"error": "An unexpected error occurred. Please try again later."}, status=500)


@api.exception_handler(HttpError)
def http_error_exception_handler(request, exc):
    """Handle HTTP errors from Django Ninja"""
    error_logger.error(
        {
            "message": str(exc),
            "path": request.path,
            "method": request.method,
            "error_type": "HttpError",
            "status_code": exc.status_code,
        }
    )
    return Response({"error": str(exc)}, status=exc.status_code)


@api.get(
    "/health",
    tags=["Health check"],
)
def health_check(request):
    """
    Health check endpoint to monitor the API's availability.

    Used for:
        - Monitoring purposes
        - Load balancing health checks
    """
    return "OK"
