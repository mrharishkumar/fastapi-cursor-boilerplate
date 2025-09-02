"""Health check service for application and database monitoring."""

from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.db import get_connection_info


class HealthCheckError(Exception):
    """Custom exception for health check failures."""


class DatabaseConnectionError(Exception):
    """Custom exception for database connection failures."""


logger = get_logger(__name__)


class HealthService:
    """
    Service class for health check operations.

    This service provides a comprehensive health check that tests:
    - Database connectivity
    - Database query performance
    - Connection information
    """

    def __init__(self, db: Session):
        """
        Initialize the health service.

        Args:
            db: Database session for health checks
        """
        self.db = db

    def health_check(self) -> dict[str, Any]:
        """
        Perform comprehensive health check
        including database connectivity and query test.

        Returns:
            dict: Health status information with database details

        Raises:
            DatabaseConnectionError: If database connection fails
        """
        logger.info("Health check requested")

        connection_info = get_connection_info()

        is_connected = connection_info["status"] == "connected"

        if not is_connected:
            logger.error("Database connection test failed")
            raise DatabaseConnectionError

        query_successful = False
        query_error_msg = None

        try:
            result = self.db.execute(text("SELECT 1 as test_value"))
            query_result = result.fetchone()
            query_successful = query_result is not None
            logger.debug("Database query test successful")
        except Exception as query_error:
            query_successful = False
            query_error_msg = str(query_error)
            logger.exception("Database query test failed")

        overall_healthy = is_connected and query_successful

        health_status = {
            "status": "healthy" if overall_healthy else "unhealthy",
            "message": (
                "All systems operational"
                if overall_healthy
                else "Some systems have issues"
            ),
            "checks": {
                "database_connection": is_connected,
                "database_query": query_successful,
            },
            "connection_info": connection_info,
        }

        if not query_successful:
            health_status["checks"]["query_error"] = query_error_msg

        if health_status["status"] == "unhealthy":
            logger.error(
                "Health check failed", extra={"health_status": health_status}
            )
        else:
            logger.info(
                "Health check successful",
                extra={"health_status": health_status},
            )

        return health_status
