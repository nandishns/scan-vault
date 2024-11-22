import uvicorn
from src.utils.logging_config import setup_logging
import logging


setup_logging()
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Server is running!")
    uvicorn.run("src.server.app:app", host="0.0.0.0", port=8000, reload=True)
