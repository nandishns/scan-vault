import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from PIL import Image
import io
import base64

from src.server.routes.scan import router
from src.server.services.scan_service import ScanService
from src.server.services.model_handler import ModelHandler
import os
import dotenv

dotenv.load_dotenv()


client = TestClient(router)


MOCK_API_KEY = os.getenv("OPENAI_API_KEY")
MOCK_RESULTS = {
    "file_name": "test.txt",
    "sensitive_fields": [
        {"type": "EMAIL", "value": "test@example.com", "confidence": "high"}
    ]
}

@pytest.fixture
def mock_scan_service():
    with patch("src.server.routes.scan.scan_service") as mock:
        yield mock

@pytest.fixture
def mock_get_api_key():
    with patch("src.server.routes.scan.get_api_key") as mock:
        mock.return_value = MOCK_API_KEY
        yield mock

class TestScanEndpoint:
    def test_scan_success(self, mock_scan_service, mock_get_api_key):
        """Test successful file scan"""
       
        mock_scan_service.scan_file.return_value = MOCK_RESULTS
        test_file = io.BytesIO(b"test content")

       
        response = client.post(
            "/scan",
            files={"file": ("test.txt", test_file)},
            headers={"X-API-Key": MOCK_API_KEY}
        )

       
        assert response.status_code == 200
        assert response.json() == {"message": "success", "results": MOCK_RESULTS}
        mock_scan_service.scan_file.assert_called_once()

    def test_scan_no_file(self, mock_scan_service, mock_get_api_key):
        """Test scan endpoint with no file"""
        response = client.post("/scan", headers={"X-API-Key": MOCK_API_KEY})
        assert response.status_code == 422

    def test_scan_service_error(self, mock_scan_service, mock_get_api_key):
        """Test scan endpoint when service raises error"""
        mock_scan_service.scan_file.side_effect = ValueError("Test error")
        test_file = io.BytesIO(b"test content")

        response = client.post(
            "/scan",
            files={"file": ("test.txt", test_file)},
            headers={"X-API-Key": MOCK_API_KEY}
        )

        assert response.status_code == 500
        assert "Test error" in response.json()["detail"]

class TestScanService:
    @pytest.fixture
    def mock_model_handler(self):
        with patch("src.server.services.scan_service.ModelHandler") as mock:
            mock_instance = Mock()
            mock_instance.predict.return_value = MOCK_RESULTS["sensitive_fields"]
            mock.create.return_value = mock_instance
            yield mock

    @pytest.fixture
    def mock_openai_client(self):
        with patch("src.server.services.scan_service.OpenAI") as mock:
            mock_instance = Mock()
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content='{"test": "result"}'))]
            mock_instance.chat.completions.create.return_value = mock_response
            mock.return_value = mock_instance
            yield mock

    @pytest.fixture
    def scan_service(self, mock_model_handler, mock_openai_client):
        with patch.dict('os.environ', {'OPENAI_API_KEY': MOCK_API_KEY}):
            return ScanService()

    @pytest.mark.asyncio
    async def test_scan_text_file(self, scan_service):
        """Test scanning text file"""
        
        mock_file = AsyncMock()
        mock_file.filename = "test.txt"
        mock_file.read.return_value = b"test content"

      
        result = await scan_service.scan_file(mock_file)

     
        assert result["file_name"] == "test.txt"
        assert "sensitive_fields" in result

    @pytest.mark.asyncio
    async def test_scan_image_file(self, scan_service):
        """Test scanning image file"""
   
        img = Image.new('RGB', (60, 30), color='red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)


        mock_file = AsyncMock()
        mock_file.filename = "test.jpg"
        mock_file.read.return_value = img_byte_arr.getvalue()

   
        result = await scan_service.scan_file(mock_file)

       
        assert result["file_name"] == "test.jpg"
        assert "sensitive_fields" in result

    @pytest.mark.asyncio
    async def test_scan_no_file(self, scan_service):
        """Test scanning with no file"""
        with pytest.raises(ValueError, match="No file provided or invalid file"):
            await scan_service.scan_file(None)

    @pytest.mark.asyncio
    async def test_scan_empty_file(self, scan_service):
        """Test scanning empty file"""
        mock_file = AsyncMock()
        mock_file.filename = "empty.txt"
        mock_file.read.return_value = b""

        result = await scan_service.scan_file(mock_file)
        assert result["sensitive_fields"] == []

    def test_validate_api_key_missing(self):
        """Test service initialization with missing API key"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': ''}):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                ScanService()

    def test_initialize_model_handler_error(self):
        """Test model handler initialization error"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': MOCK_API_KEY}):
            with patch('src.server.services.scan_service.ModelHandler.create') as mock_create:
                mock_create.side_effect = Exception("Model init error")
                with pytest.raises(ValueError, match="Model handler initialization failed"):
                    ScanService()

    @pytest.mark.asyncio
    async def test_process_image_error(self, scan_service):
        """Test image processing error"""
        mock_file = AsyncMock()
        mock_file.filename = "test.jpg"
        mock_file.read.side_effect = Exception("Image processing error")

        with pytest.raises(ValueError, match="Error processing image"):
            await scan_service._process_image(mock_file)

    def test_analyze_image_with_gpt_error(self, scan_service):
        """Test GPT image analysis error"""
        with patch.object(scan_service.client.chat.completions, 'create') as mock_create:
            mock_create.side_effect = Exception("GPT analysis error")
            result = scan_service._analyze_image_with_gpt("mock_base64")
            assert result == {"file_name": None, "sensitive_fields": []}
