"""Configuration management for the FastAPI application.

This module provides centralized configuration management using Pydantic
settings. It handles database configuration, CORS settings, logging
configuration, and environment variable validation for the application.
"""

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration.

    This class manages all application configuration including database
    settings, CORS origins, logging configuration, and security parameters.
    It provides validation for critical settings and generates database
    connection strings.
    """

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Cursor Boilerplate"
    VERSION: str = "0.1.0"

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        """Assemble CORS origins from string or list.

        Args:
            v: CORS origins as string or list

        Returns:
            Processed CORS origins as list or string

        Raises:
            ValueError: If the input format is invalid
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, list | str):
            return v
        raise ValueError(v)

    # Database Configuration for pyodbc
    DATABASE_DRIVER: str = "ODBC Driver 18 for SQL Server"
    DATABASE_SERVER: str = "localhost"
    DATABASE_NAME: str = "fastapi_db"
    DATABASE_USERNAME: str = "sa"
    DATABASE_PASSWORD: str = "your_secure_password_here"
    DATABASE_TRUSTED_CONNECTION: bool = False

    # Database Security Settings
    DATABASE_ENCRYPT: bool = True
    DATABASE_TRUST_SERVER_CERTIFICATE: bool = False
    DATABASE_CERTIFICATE_PATH: str = ""
    DATABASE_CONNECTION_TIMEOUT: int = 30
    DATABASE_COMMAND_TIMEOUT: int = 30

    # Connection Pool Settings
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600

    # Legacy DATABASE_URL for compatibility
    DATABASE_URL: str = ""

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE_MAX_SIZE: str = "10 MB"
    LOG_FILE_RETENTION: str = "30 days"

    @property
    def database_connection_string(self) -> str:
        """Generate pyodbc connection string from individual components.

        This property constructs a complete database connection string
        from the individual configuration components, including security
        settings and connection parameters.

        Returns:
            Complete database connection string for pyodbc
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL

        base_connection = self._build_base_connection()
        security_params = self._build_security_parameters()

        if security_params:
            return f"{base_connection};{security_params}"
        return base_connection

    def _build_base_connection(self) -> str:
        """Build the base database connection string.

        Returns:
            Base connection string without security parameters
        """
        if self.DATABASE_TRUSTED_CONNECTION:
            return (
                f"DRIVER={self.DATABASE_DRIVER};"
                f"SERVER={self.DATABASE_SERVER};"
                f"DATABASE={self.DATABASE_NAME};"
                f"Trusted_Connection=yes"
            )

        return (
            f"DRIVER={self.DATABASE_DRIVER};"
            f"SERVER={self.DATABASE_SERVER};"
            f"DATABASE={self.DATABASE_NAME};"
            f"UID={self.DATABASE_USERNAME};"
            f"PWD={self.DATABASE_PASSWORD}"
        )

    def _build_security_parameters(self) -> str:
        """Build security and connection parameters string.

        Returns:
            Semicolon-separated security parameters string
        """
        security_params = []

        encrypt_value = "yes" if self.DATABASE_ENCRYPT else "no"
        security_params.append(f"Encrypt={encrypt_value}")

        trust_cert_value = (
            "yes" if self.DATABASE_TRUST_SERVER_CERTIFICATE else "no"
        )
        security_params.append(f"TrustServerCertificate={trust_cert_value}")

        security_params.append(
            f"Connection Timeout={self.DATABASE_CONNECTION_TIMEOUT}"
        )
        security_params.append(
            f"Command Timeout={self.DATABASE_COMMAND_TIMEOUT}"
        )

        if self.DATABASE_CERTIFICATE_PATH:
            security_params.append(
                f"Certificate={self.DATABASE_CERTIFICATE_PATH}"
            )

        return ";".join(security_params)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
