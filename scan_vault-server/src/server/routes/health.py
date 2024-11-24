import logging
import time
from fastapi import APIRouter


router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/health")
async def health():
    """Endpoint to check the health of the server."""
    logger.info("Health check endpoint called successfully", extra={"timestamp": time.time()})
    return {"status": "ok"}
