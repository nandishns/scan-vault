import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from firebase_admin import firestore

from src.server.routes.save_detection import router
from src.services.firebase_service import FirebaseService


client = TestClient(router)


MOCK_DETECTION_DATA = {
    "file_name": "test.txt",
    "sensitive_fields": [
        {"type": "EMAIL", "value": "test@example.com", "confidence": "high"}
    ]
}

MOCK_FIRESTORE_DATA = {
    "fileName": "test.txt",
    "sensitiveInfo": [
        {"type": "EMAIL", "value": "test@example.com", "confidence": "high"}
    ],
    "createdAt": firestore.SERVER_TIMESTAMP,
}

@pytest.fixture
def mock_firebase_service():
    with patch("src.server.routes.save_detection.FirebaseService") as mock:
        mock_instance = Mock()
        mock_instance.save_detection = AsyncMock()
        mock.return_value = mock_instance
        yield mock_instance

class TestSaveDetectionEndpoint:
    def test_save_detection_success(self, mock_firebase_service):
        """Test successful detection save"""
     
        mock_firebase_service.save_detection.return_value = "mock_doc_id"

     
        response = client.post("/save-detection", json=MOCK_DETECTION_DATA)
 
        assert response.status_code == 201
        assert response.json() == {
            "message": "Detection saved successfully",
            "id": "mock_doc_id"
        }
        mock_firebase_service.save_detection.assert_called_once()

    def test_save_detection_missing_data(self, mock_firebase_service):
        """Test save detection with missing required fields"""
       
        invalid_data = {"file_name": "test.txt"}
        response = client.post("/save-detection", json=invalid_data)
        
        assert response.status_code == 400
        assert "Missing required data" in response.json()["error"]
        mock_firebase_service.save_detection.assert_not_called()

    def test_save_detection_empty_data(self, mock_firebase_service):
        """Test save detection with empty data"""
        response = client.post("/save-detection", json={})
        
        assert response.status_code == 400
        assert "Missing required data" in response.json()["error"]
        mock_firebase_service.save_detection.assert_not_called()

    def test_save_detection_service_error(self, mock_firebase_service):
        """Test save detection when service fails"""
       
        mock_firebase_service.save_detection.return_value = None

        
        response = client.post("/save-detection", json=MOCK_DETECTION_DATA)

        
        assert response.status_code == 500
        assert "Failed to save detection" in response.json()["error"]

class TestFirebaseService:
    @pytest.fixture
    def mock_firebase_admin(self):
        with patch("firebase_admin.initialize_app") as mock_init:
            yield mock_init

    @pytest.fixture
    def mock_firestore_client(self):
        with patch("firebase_admin.firestore.client") as mock_client:
            mock_db = Mock()
            mock_client.return_value = mock_db
            yield mock_db

    @pytest.fixture
    def mock_credentials(self):
        with patch("firebase_admin.credentials.Certificate") as mock_cred:
            yield mock_cred

    def test_firebase_service_singleton(self, mock_firebase_admin, mock_firestore_client, mock_credentials):
        """Test FirebaseService singleton pattern"""
        service1 = FirebaseService()
        service2 = FirebaseService()
        assert service1 is service2

    def test_firebase_service_initialization_error(self, mock_firebase_admin, mock_credentials):
        """Test FirebaseService initialization error"""
        mock_firebase_admin.side_effect = Exception("Init error")
        
        with pytest.raises(Exception, match="Init error"):
            FirebaseService()

    @pytest.mark.asyncio
    async def test_save_detection_success(self, mock_firestore_client):
        """Test successful detection save"""
      
        mock_doc = Mock()
        mock_doc.id = "mock_doc_id"
        mock_collection = Mock()
        mock_collection.document.return_value = mock_doc
        mock_firestore_client.collection.return_value = mock_collection

        service = FirebaseService()
        

        result = await service.save_detection(MOCK_FIRESTORE_DATA)

     
        assert result == "mock_doc_id"
        mock_firestore_client.collection.assert_called_with("detections")
        mock_doc.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_detection_error(self, mock_firestore_client):
        """Test detection save error"""
      
        mock_firestore_client.collection.side_effect = Exception("Database error")
        
        service = FirebaseService()
        
     
        result = await service.save_detection(MOCK_FIRESTORE_DATA)

        
        assert result is None

    @pytest.mark.asyncio
    async def test_get_detections_success(self, mock_firestore_client):
        """Test successful detections retrieval"""
      
        mock_doc = Mock()
        mock_doc.to_dict.return_value = MOCK_FIRESTORE_DATA
        mock_doc.id = "mock_doc_id"
        mock_firestore_client.collection().get.return_value = [mock_doc]

        service = FirebaseService()
        
      
        result = await service.get_detections()

       
        assert len(result) == 1
        assert result[0]["id"] == "mock_doc_id"
        mock_firestore_client.collection.assert_called_with("detections")

    @pytest.mark.asyncio
    async def test_get_detections_error(self, mock_firestore_client):
        """Test detections retrieval error"""
        
        mock_firestore_client.collection().get.side_effect = Exception("Database error")
        
        service = FirebaseService()
        
       
        result = await service.get_detections()

       
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_detection_success(self, mock_firestore_client):
        """Test successful detection deletion"""
        service = FirebaseService()
        await service.delete_detection("mock_doc_id")
        
        mock_firestore_client.collection.assert_called_with("detections")
        mock_firestore_client.collection().document.assert_called_with("mock_doc_id")
        mock_firestore_client.collection().document().delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_detection_error(self, mock_firestore_client):
        """Test detection deletion error"""
      
        mock_firestore_client.collection().document().delete.side_effect = Exception("Delete error")
        
        service = FirebaseService()
        
        with pytest.raises(Exception, match="Delete error"):
            await service.delete_detection("mock_doc_id")
