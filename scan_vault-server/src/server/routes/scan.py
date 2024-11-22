from fastapi import APIRouter, File, UploadFile, HTTPException
import logging

from fastapi.params import Depends

from src.server.models.scan_request import ScanRequest
from src.server.services.scan_service import ScanService
from src.utils.auth import get_api_key

logger = logging.getLogger(__name__)
scan_service = ScanService()

router = APIRouter();

@router.post("/scan",dependencies=[Depends(get_api_key)])
async def scan(file: UploadFile = File(...),):
    """Endpoint to scan uploaded files."""
    try:
        results = await scan_service.scan_file(file)
        return {"message": "File scanned successfully!", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

