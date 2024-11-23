import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import s3fs
import logging  

logger = logging.getLogger(__name__)

s3fs.S3FileSystem.cachable = False

API_KEY = os.environ['SCAN_VAULT_API_KEY']
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
  if not verify_key(api_key):
    logger.error("Invalid API Key: Unauthorized access attempt")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid API Key")

def verify_key(api_key: str):
  return api_key == API_KEY


