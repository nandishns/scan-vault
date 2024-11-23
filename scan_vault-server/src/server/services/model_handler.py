from typing import List, Dict, Optional, Union
import logging
from openai import OpenAI
import base64
from io import BytesIO
from src.server.utils.analysis_prompts import AnalysisPrompts
from src.server.utils.json_parser import JSONParser

logger = logging.getLogger(__name__)

class LLMHandler:
    """Handles all Large Language Model (LLM) interactions including text and vision analysis."""
    
    def __init__(self, api_key: str):
        """
        Initialize the LLM handler.
        
        Args:
            api_key (str): OpenAI API key for authentication
            
        Raises:
            ValueError: If API key is invalid or initialization fails
        """
        self._validate_api_key(api_key)
        self.client = self._initialize_client(api_key)
        self.json_parser = JSONParser()

    def _validate_api_key(self, api_key: str) -> None:
        """
        Validate the OpenAI API key.
        
        Args:
            api_key (str): API key to validate
            
        Raises:
            ValueError: If API key is missing or invalid
        """
        if not api_key:
            logger.error("OpenAI API key not provided")
            raise ValueError("OpenAI API key is required")

    def _initialize_client(self, api_key: str) -> OpenAI:
        """
        Initialize the OpenAI client.
        
        Args:
            api_key (str): Valid OpenAI API key
            
        Returns:
            OpenAI: Initialized OpenAI client
            
        Raises:
            ValueError: If client initialization fails
        """
        try:
            return OpenAI(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")

    def analyze_text(self, text: str) -> List[Dict]:
        """
        Analyze text content for sensitive information.
        
        Args:
            text (str): Text content to analyze
            
        Returns:
            List[Dict]: List of detected sensitive information
            
        Raises:
            ValueError: If analysis fails
        """
        try:
            logger.info("Starting text analysis")
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": AnalysisPrompts.SYSTEM_ROLE},
                    {"role": "user", "content": f"{AnalysisPrompts.TEXT_ANALYSIS}\n\n{text}"}
                ],
                max_tokens=1000
            )
            
            if not response.choices:
                logger.error("No response received from GPT")
                raise ValueError("No response received from model")

            content = response.choices[0].message.content.strip()
            results = self.json_parser.parse_gpt_response(content)
            logger.info("Text analysis completed successfully")
            return results

        except Exception as e:
            logger.error(f"Error in text analysis: {e}")
            raise ValueError(f"Failed to analyze text: {str(e)}")

    def analyze_image(self, image_data: bytes) -> List[Dict]:
        """
        Analyze image content for sensitive information using Vision API.
        
        Args:
            image_data (bytes): Raw image data
            
        Returns:
            List[Dict]: List of detected sensitive information
            
        Raises:
            ValueError: If image analysis fails
        """
        try:
            logger.info("Starting image analysis")
            # Convert image to base64
            img_str = base64.b64encode(image_data).decode()
            
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": AnalysisPrompts.TEXT_ANALYSIS},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_str}",
                                    "detail": "high"
                                }
                            }
                        ]
                    },
                    {
                        "role": "system",
                        "content": AnalysisPrompts.SYSTEM_ROLE
                    }
                ],
                max_tokens=1000
            )

            if not response.choices:
                logger.error("No response received from Vision API")
                raise ValueError("No response received from model")

            content = response.choices[0].message.content.strip()
            results = self.json_parser.parse_gpt_response(content)
            logger.info("Image analysis completed successfully")
            return results

        except Exception as e:
            logger.error(f"Error in image analysis: {e}")
            raise ValueError(f"Failed to analyze image: {str(e)}")
