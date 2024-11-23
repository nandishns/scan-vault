from fastapi import APIRouter, Depends
from firebase_admin import firestore
from typing import Dict, Any
from src.utils.auth import get_api_key

from src.services.firebase_service import FirebaseService

router = APIRouter()

@router.post("/save-detection", dependencies=[Depends(get_api_key)])
async def save_detection(detection_data: Dict[str, Any]):
    try:
        print(detection_data)
        # Validate required fields
        if not detection_data or 'sensitive_fields' not in detection_data:
            return {'error': 'Missing required data'}, 400
            
        # Create a new document in the 'detections' collection
        firebase_service = FirebaseService()
        doc_id = await firebase_service.save_detection({
            'fileName': detection_data['file_name'],
            'sensitiveInfo': detection_data['sensitive_fields'],
            'createdAt': firestore.SERVER_TIMESTAMP,
        })
        if not doc_id:
            return {'error': 'Failed to save detection'}, 500

        return {'message': 'Detection saved successfully', 'id': doc_id}, 201
        
    except Exception as e:
        return {'error': str(e)}, 500
