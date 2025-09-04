"""Database connection and session management using pyodbc."""

from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager
from urllib.parse import quote_plus

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Manages database engine and session factory."""

    def __init__(self) -> None:
        """Initialize the DatabaseManager."""
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None

    def create_database_engine(self) -> Engine:
        """Create and configure the SQLAlchemy engine with pyodbc."""
        try:
            engine = create_engine(
                f"mssql+pyodbc:///?odbc_connect="
                f"{quote_plus(settings.database_connection_string)}",
                pool_size=settings.DATABASE_POOL_SIZE,
                max_overflow=settings.DATABASE_MAX_OVERFLOW,
                pool_timeout=settings.DATABASE_POOL_TIMEOUT,
                pool_recycle=settings.DATABASE_POOL_RECYCLE,
                pool_pre_ping=True,
                echo=False,
            )

            @event.listens_for(engine, "connect")
            def set_sqlite_pragma(dbapi_connection, _connection_record) -> None:
                """Set connection-specific parameters."""
                dbapi_connection.autocommit = True

            @event.listens_for(engine, "checkout")
            def receive_checkout(
                _dbapi_connection,
                _connection_record,
                _connection_proxy,
            ) -> None:
                """Log when a connection is checked out from the pool."""
                logger.debug("Connection checked out from pool")

            @event.listens_for(engine, "checkin")
            def receive_checkin(_dbapi_connection, _connection_record) -> None:
                """Log when a connection is checked back into the pool."""
                logger.debug("Connection checked back into pool")

            logger.info("Database engine created successfully")
        except Exception:
            logger.exception("Failed to create database engine")
            raise
        else:
            return engine

    def get_engine(self) -> Engine:
        """Get the database engine, creating it if necessary."""
        if self._engine is None:
            self._engine = self.create_database_engine()
        return self._engine

    def get_session_factory(self) -> sessionmaker[Session]:
        """Get the session factory, creating it if necessary."""
        if self._session_factory is None:
            engine = self.get_engine()
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
            )
        return self._session_factory

    def close_connections(self) -> None:
        """Close all database connections and cleanup resources."""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            logger.info("Database engine disposed")
        self._session_factory = None


db_manager = DatabaseManager()


def get_engine() -> Engine:
    """Get the database engine, creating it if necessary."""
    return db_manager.get_engine()


def get_session_factory() -> sessionmaker[Session]:
    """Get the session factory, creating it if necessary."""
    return db_manager.get_session_factory()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.

    Yields:
        Session: SQLAlchemy database session

    Raises:
        SQLAlchemyError: If database connection fails
    """
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
    except SQLAlchemyError:
        logger.exception("Database session error")
        session.rollback()
        raise
    except Exception:
        logger.exception("Unexpected error in database session")
        session.rollback()
        raise
    finally:
        session.close()


@asynccontextmanager
async def get_async_db() -> AsyncGenerator[Session, None]:
    """
    Async context manager for database sessions.

    Yields:
        Session: SQLAlchemy database session

    Raises:
        SQLAlchemyError: If database connection fails
    """
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
    except SQLAlchemyError:
        logger.exception("Database session error")
        session.rollback()
        raise
    except Exception:
        logger.exception("Unexpected error in database session")
        session.rollback()
        raise
    finally:
        session.close()


def get_connection_info() -> dict[str, str]:
    """
    Get database connection status information for health monitoring.

    Returns:
        dict[str, str]: Connection status information.
    """
    try:
        engine = get_engine()
        connection_status = "configured"

        with engine.connect() as connection:
            connection.execute(text("SELECT 1 as test_value"))
            connection_status = "connected"

    except Exception:
        logger.exception("Database connection test failed:")
        connection_status = "failed"

    return {
        "status": connection_status,
        "pool_configured": "yes" if settings.DATABASE_POOL_SIZE else "no",
        "connection_test": (
            "passed" if connection_status == "connected" else "failed"
        ),
    }


def close_connections() -> None:
    """Close all database connections and cleanup resources."""
    db_manager.close_connections()


logger.info(
    "Database module loaded - connections will be established when first "
    "accessed"
)
