from typing import Dict, Union
import logging
import os
from PIL import Image
import base64
from io import BytesIO
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
from src.server.services.model_handler import ModelHandler
from src.server.utils.file_processor import FileProcessor
from src.server.utils.analysis_prompts import AnalysisPrompts
from src.server.utils.json_parser import JSONParser

logger = logging.getLogger(__name__)

class ScanService:
    """Service for scanning files for sensitive information."""
    
    def __init__(self,):
        """Initialize scan service with necessary components."""
        self._validate_api_key(os.getenv("OPENAI_API_KEY"))
        self.model_handler = self._initialize_model_handler(os.getenv("OPENAI_API_KEY"))
        self.file_processor = FileProcessor()
        self.json_parser = JSONParser()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _validate_api_key(self, api_key: str) -> None:
        """Validate OpenAI API key."""
        if not api_key:
            logger.error("OpenAI API key not found")
            raise ValueError("OpenAI API key is required")

    def _initialize_model_handler(self, api_key: str) -> ModelHandler:
        """Initialize the model handler."""
        try:
            return ModelHandler.create(
                handler_type="gpt",
                api_key=api_key
            )
        except Exception as e:
            logger.error(f"Failed to initialize model handler: {e}")
            raise ValueError(f"Model handler initialization failed: {e}")

    async def scan_file(self, file) -> Dict:
        """Handle end-to-end scanning process."""
        if not file or not file.filename:
            raise ValueError("No file provided or invalid file")

        try:
            file_extension = self.file_processor.get_file_extension(file.filename)
            
            # Process image files with Vision API
            if file_extension in ["jpg", "jpeg", "png", "bmp"]:
                return await self._process_image(file)
            
            # Process text-based files
            content = await self._process_file_content(file, file_extension)
            if not content:
                logger.warning(f"No content extracted from file: {file.filename}")
                return self._empty_result(file.filename)

            results = self.model_handler.predict(content)
            return {
                "file_name": file.filename,
                "sensitive_fields": results
            }

        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {e}")
            raise ValueError(f"Error processing file: {str(e)}")

    async def _process_image(self, file) -> Dict:
        """Process image using GPT Vision API."""
        try:
            content = await file.read()
            image = Image.open(BytesIO(content))
            
            # Convert image to base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            vision_result = self._analyze_image_with_gpt(img_str)
            return {
                "file_name": file.filename,
                "sensitive_fields": vision_result
            }

        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise ValueError(f"Error processing image: {str(e)}")

    def _analyze_image_with_gpt(self, base64_image: str) -> Dict:
        """Analyze image using GPT-4 Vision."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-05-13",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": AnalysisPrompts.TEXT_ANALYSIS},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high",
                                },
                            },
                        ],
                    },
                    {
                        "role": "system",
                        "content": AnalysisPrompts.SYSTEM_ROLE
                    }
                ],
                max_tokens=1000,
            )
            
            # Parse response and remove escape characters
            content = response.choices[0].message.content.strip()
            content = content.replace('\\n', '\n').replace('\\', '')
            
            # Parse the content using JSONParser
            parsed_content = self.json_parser.parse_gpt_response(content)
            return parsed_content
            
        except Exception as e:
            logger.error(f"Error in GPT Vision analysis: {e}")
            return self._empty_result()

    async def _process_file_content(self, file, file_extension: str) -> str:
        """Process file content based on file type."""
        try:
            return await self.file_processor.process_file(file, file_extension)
        except Exception as e:
            logger.error(f"Error processing file content: {e}")
            raise ValueError(f"Error processing file content: {str(e)}")

    def _empty_result(self, filename: str = None) -> Dict:
        """Return empty result structure."""
        return {
            "file_name": filename,
            "sensitive_fields": {
                "pii": [],
                "phi": [],
                "pci": []
            }
        }
