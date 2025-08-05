import os
import sys
from loguru import logger


def configure_logging(level: str = "INFO", request_id: str | None = None) -> None:
    """Configure the global Loguru logger with JSON output.

    Parameters
    ----------
    level: str
        Logging level to use.
    request_id: str | None
        Identifier of the request, propagated to all log records.
    """
    logger.remove()
    log_file = os.environ.get("LOG_FILE", "agent.log")
    logger.add(sys.stdout, level=level, serialize=True)
    logger.add(log_file, level=level, rotation="1 MB", serialize=True)
    logger.configure(extra={"request_id": request_id})
