from fastapi import APIRouter, Depends
from src.services.firebase_service import FirebaseService
from src.utils.auth import get_api_key

router = APIRouter()


@router.get("/get-saved-detections", dependencies=[Depends(get_api_key)])
async def get_detections():
    try:
        firebase_service = FirebaseService()
        detections = await firebase_service.get_detections()
        if detections is None:
            return {"detections": []}, 200
        return {"detections": detections}, 200
    except Exception as e:
        return {"error": str(e)}, 500
