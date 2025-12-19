import logging
import sys
from datetime import datetime
from typing import Any, Dict
from enum import Enum
from fastapi import HTTPException
import traceback


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger:
    def __init__(self, name: str = "AI-Textbook-API", level: LogLevel = LogLevel.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.value))

        # Prevent adding multiple handlers if logger already has handlers
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, level.value))

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)

            # Add handler to logger
            self.logger.addHandler(console_handler)

    def debug(self, message: str, extra: Dict[str, Any] = None):
        self._log(logging.DEBUG, message, extra)

    def info(self, message: str, extra: Dict[str, Any] = None):
        self._log(logging.INFO, message, extra)

    def warning(self, message: str, extra: Dict[str, Any] = None):
        self._log(logging.WARNING, message, extra)

    def error(self, message: str, extra: Dict[str, Any] = None):
        self._log(logging.ERROR, message, extra)

    def critical(self, message: str, extra: Dict[str, Any] = None):
        self._log(logging.CRITICAL, message, extra)

    def _log(self, level: int, message: str, extra: Dict[str, Any] = None):
        if extra:
            message = f"{message} | Extra: {extra}"
        self.logger.log(level, message)

    def log_exception(self, message: str = "An exception occurred"):
        """Log the current exception with traceback"""
        self.error(f"{message} | Traceback: {traceback.format_exc()}")


class ErrorHandling:
    @staticmethod
    def handle_error(error: Exception, logger: Logger = None, error_code: int = 500):
        """Standardized error handling"""
        if logger:
            logger.log_exception(f"Error occurred: {str(error)}")

        # Return appropriate HTTP exception based on error type
        if isinstance(error, HTTPException):
            raise error
        else:
            raise HTTPException(status_code=error_code, detail=str(error))

    @staticmethod
    def create_error_response(error_type: str, message: str, details: Any = None):
        """Create standardized error response"""
        return {
            "error": {
                "type": error_type,
                "message": message,
                "details": details,
                "timestamp": datetime.utcnow().isoformat(),
            }
        }


# Global logger instance
api_logger = Logger()


def get_logger(name: str = "AI-Textbook-API") -> Logger:
    """Get a logger instance"""
    return Logger(name=name)