from typing import Dict, Union
import logging
import os
from PIL import Image
import base64
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

from src.server.utils.file_processor import FileProcessor
from src.server.utils.analysis_prompts import AnalysisPrompts
from src.server.utils.json_parser import JSONParser

logger = logging.getLogger(__name__)

class ScanService:
    """Service for scanning files for sensitive information."""
    
    def __init__(self,):
        """Initialize scan service with necessary components."""
        api_key = os.getenv("OPENAI_API_KEY")
        self._validate_api_key(api_key)
        self.client = OpenAI(api_key=api_key)
        self.file_processor = FileProcessor()
        self.json_parser = JSONParser()

    def _validate_api_key(self, api_key: str) -> None:
        """Validate OpenAI API key."""
        if not api_key:
            logger.error("OpenAI API key not found")
            raise ValueError("OpenAI API key is required")

    async def scan_file(self, file) -> Dict:
        """
        Handle end-to-end scanning process for both text and image files.
        
        Args:
            file: File object to scan
            
        Returns:
            Dict: Scan results including file name and detected sensitive fields
            
        Raises:
            ValueError: If file processing fails
        """
        if not file or not file.filename:
            raise ValueError("No file provided or invalid file")

        try:
            file_extension = self.file_processor.get_file_extension(file.filename)
            
            # Process image files
            if file_extension.lower() in ["jpg", "jpeg", "png", "bmp"]:
                content = await file.read()
                results = self.llm_handler.analyze_image(content)
            else:
                # Process text-based files
                content = await self._process_file_content(file, file_extension)
                if not content:
                    logger.warning(f"No content extracted from file: {file.filename}")
                    return self._empty_result(file.filename)
                    
                results = self.llm_handler.analyze_text(content)

            return {
                "file_name": file.filename,
                "sensitive_fields": results
            }

        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {e}")
            raise ValueError(f"Error processing file: {str(e)}")

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
            "sensitive_fields": []
        }
