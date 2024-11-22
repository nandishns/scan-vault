from firebase_admin import firestore
from fastapi import APIRouter
from typing import Dict, Any

from services.firebase_service import FirebaseService

router = APIRouter()

@router.post("/save-detection")
async def save_detection(detection_data: Dict[str, Any]):
    try:
        # Validate required fields
        if not detection_data or 'detectedContent' not in detection_data:
            return {'error': 'Missing required data'}, 400
            
        # Create a new document in the 'detections' collection
        firebase_service = FirebaseService()
        doc_id = await firebase_service.save_detection({
            'content': detection_data['detectedContent']
        })
        if not doc_id:
            return {'error': 'Failed to save detection'}, 500

        return {'message': 'Detection saved successfully', 'id': doc_id}, 201
        
    except Exception as e:
        return {'error': str(e)}, 500
