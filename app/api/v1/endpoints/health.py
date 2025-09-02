"""Health check endpoints for monitoring application and database status."""

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

from app.core.config import settings
from app.core.logging import get_logger
from app.db import get_connection_info

logger = get_logger(__name__)
router = APIRouter()


def _get_service_status() -> dict[str, Any]:
    """Get basic service status information.

    Returns:
        dict: Service status information
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(UTC).isoformat(),
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }


def _get_database_status() -> dict[str, Any]:
    """Get database connection status.

    Returns:
        dict: Database status information
    """
    try:
        connection_info = get_connection_info()
        if connection_info["status"] == "connected":
            return {
                "status": "connected",
                "pool_configured": connection_info.get(
                    "pool_configured", "unknown"
                ),
                "connection_test": connection_info.get(
                    "connection_test", "unknown"
                ),
            }
        return {
            "status": "error",
            "pool_configured": connection_info.get(
                "pool_configured", "unknown"
            ),
            "connection_test": connection_info.get(
                "connection_test", "unknown"
            ),
        }
    except Exception:
        logger.exception("Failed to get database connection status")
        return {
            "status": "error",
            "pool_configured": "unknown",
            "connection_test": "failed",
        }


@router.get("/", tags=["health"])
async def health_check() -> dict[str, Any]:
    """
    Comprehensive health check endpoint.

    This endpoint provides both service and database health status
    in a single response. It's designed for monitoring systems,
    load balancers, and health dashboards.

    Returns:
        dict: Complete health status including service and database status
    """
    logger.info("Health check requested")

    service_status = _get_service_status()

    database_status = _get_database_status()

    overall_healthy = (
        service_status["status"] == "ok"
        and database_status["status"] == "connected"
    )

    if database_status["status"] == "error":
        logger.warning(
            "Database health check indicates issues",
            extra={"database_status": database_status},
        )

    if not overall_healthy:
        logger.warning(
            "Overall health check indicates issues",
            extra={
                "service_status": service_status,
                "database_status": database_status,
            },
        )

    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "message": (
            "All systems operational"
            if overall_healthy
            else "Some systems have issues"
        ),
        "timestamp": service_status["timestamp"],
        "service": service_status,
        "database": database_status,
    }
