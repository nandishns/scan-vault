from fastapi import APIRouter

from src.services.firebase_service import FirebaseService


router = APIRouter()

@router.delete("/delete-detection/{detection_id}")
async def delete_detection(detection_id: str):
    print(f"Deleting detection with ID: {detection_id}")
    try:
        firebase_service = FirebaseService()
        await firebase_service.delete_detection(detection_id)
        return {"message": "Detection deleted successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
