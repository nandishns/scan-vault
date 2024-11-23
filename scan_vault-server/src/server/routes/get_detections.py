from fastapi import APIRouter
from src.services.firebase_service import FirebaseService

router = APIRouter()

@router.get("/get-saved-detections")
async def get_detections():
    try:
        firebase_service = FirebaseService()
        detections = await firebase_service.get_detections()
        if detections is None:
            return {"detections": []}, 200
        return {"detections": detections}, 200
    except Exception as e:
        return {"error": str(e)}, 500
