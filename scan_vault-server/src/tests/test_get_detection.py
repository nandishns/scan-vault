import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock

from src.server.routes.get_detections import router


client = TestClient(router)


MOCK_DETECTIONS = [
    {
        "id": "123",
        "timestamp": "2024-03-14T12:00:00Z",
        "file_name": "test.txt",
        "sensitive_fields": [
            {"type": "EMAIL", "value": "test@example.com", "confidence": "high"}
        ]
    }
]

@pytest.fixture
def mock_firebase_service():
    with patch("src.server.routes.get_detections.FirebaseService") as mock:
        mock_instance = Mock()
       
        mock_instance.get_detections = AsyncMock()
        mock.return_value = mock_instance
        yield mock_instance

class TestGetDetectionsEndpoint:
    def test_get_detections_success(self, mock_firebase_service):
        """Test successful retrieval of detections"""
       
        mock_firebase_service.get_detections.return_value = MOCK_DETECTIONS

      
        response = client.get("/get-saved-detections")

    
        assert response.status_code == 200
        assert response.json() == {"detections": MOCK_DETECTIONS}
        mock_firebase_service.get_detections.assert_called_once()

    def test_get_detections_empty(self, mock_firebase_service):
        """Test when no detections are found"""
      
        mock_firebase_service.get_detections.return_value = None

      
        response = client.get("/get-saved-detections")

     
        assert response.status_code == 200
        assert response.json() == {"detections": []}
        mock_firebase_service.get_detections.assert_called_once()

    def test_get_detections_error(self, mock_firebase_service):
        """Test error handling"""
        
        mock_firebase_service.get_detections.side_effect = Exception("Database error")

       
        response = client.get("/get-saved-detections")

        
        assert response.status_code == 500
        assert response.json() == {"error": "Database error"}
        mock_firebase_service.get_detections.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_detections_async_behavior(self, mock_firebase_service):
        """Test async behavior of the endpoint"""
       
        mock_firebase_service.get_detections.return_value = MOCK_DETECTIONS

        response = client.get("/get-saved-detections")

        
        assert response.status_code == 200
       
        mock_firebase_service.get_detections.assert_awaited_once()
