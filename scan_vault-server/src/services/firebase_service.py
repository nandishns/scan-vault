import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FirebaseService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Firebase Admin SDK and Firestore client"""
        try:
            # Initialize Firebase Admin SDK
            cred = credentials.Certificate("serviceAccount.json")
            firebase_admin.initialize_app(cred)
            
            # Initialize Firestore client
            self.db = firestore.client()
            logger.info("Firebase initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise
    
    async def save_detection(self, detection_data: Dict[str, Any]) -> Optional[str]:
        """
        Save detection data to Firestore
        
        Args:
            detection_data (Dict[str, Any]): Detection data to save
            
        Returns:
            Optional[str]: Document ID if successful, None if failed
        """
        try:
            # Add timestamp
            detection_data['timestamp'] = datetime.utcnow()
            
            # Create a new document in the detections collection
            doc_ref = self.db.collection('detections').document()
            doc_ref.set(detection_data)
            
            logger.info(f"Detection saved successfully with ID: {doc_ref.id}")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"Error saving detection: {str(e)}")
            return None
    
    async def get_detection(self, detection_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a detection by ID
        
        Args:
            detection_id (str): The ID of the detection to retrieve
            
        Returns:
            Optional[Dict[str, Any]]: Detection data if found, None if not found
        """
        try:
            doc_ref = self.db.collection('detections').document(detection_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving detection: {str(e)}")
            return None 