from typing import List, Dict, Optional
import logging
from openai import OpenAI
import json
from abc import ABC, abstractmethod
from src.server.utils.analysis_prompts import AnalysisPrompts
from src.server.utils.json_parser import JSONParser

logger = logging.getLogger(__name__)

class ModelInterface(ABC):
    """Abstract base class for all model handlers."""
    @abstractmethod
    def predict(self, text: str) -> List[Dict]:
        """Run predictions on the provided text."""
        pass

    
@DeprecationWarning
class SpacyModelHandler(ModelInterface):
    """Deprecated: Legacy Spacy-based model handler."""
    def __init__(self, model_path: str):
        import spacy  # Import here to make it optional
        logger.warning("SpacyModelHandler is deprecated. Please use GPTModelHandler instead.")
        self.nlp = spacy.load(model_path)
    @DeprecationWarning
    def predict(self, text: str) -> List[Dict]:
        """Deprecated method using Spacy for predictions."""
        doc = self.nlp(text)
        results = []
        for ent in doc.ents:
            results.append({
                "type": ent.label_,
                "value": ent.text,
                "confidence": "medium",
                "context": "Found using deprecated Spacy model"
            })
        return results

class GPTModelHandler(ModelInterface):
    """Modern GPT-based model handler for sensitive information detection."""
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self._validate_api_key(api_key)
        self.client = self._initialize_client(api_key)
        self.model = model
        self.json_parser = JSONParser()

    def _validate_api_key(self, api_key: str) -> None:
        """Validate the API key."""
        if not api_key:
            raise ValueError("OpenAI API key is required")

    def _initialize_client(self, api_key: str) -> OpenAI:
        """Initialize the OpenAI client."""
        try:
            return OpenAI(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise ValueError(f"Failed to initialize OpenAI client: {e}")

    def predict(self, text: str) -> List[Dict]:
        """Run GPT analysis on the provided text."""
        try:
            response = self._get_gpt_response(text)
            if not response.choices:
                raise ValueError("No response received from GPT")

            result = self.json_parser.parse_gpt_response(response.choices[0].message.content)
            return self._flatten_results(result)

        except Exception as e:
            logger.error(f"Error in GPT prediction: {e}")
            raise ValueError(f"Failed to analyze text: {e}")

    def _get_gpt_response(self, text: str):
        """Get response from GPT model."""
        return self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": AnalysisPrompts.SYSTEM_ROLE},
                {"role": "user", "content": f"{AnalysisPrompts.TEXT_ANALYSIS}\n\nText to analyze:\n{text}"}
            ],
            temperature=0.3,
            max_tokens=1000
        )

    def _flatten_results(self, results: Dict) -> List[Dict]:
        """Convert nested results into a flat list."""
        flattened = []
        for category, items in results.items():
            for item in items:
                item['category'] = category.upper()
                flattened.append(item)
        return flattened

class ModelHandler:
    """Factory class for creating appropriate model handlers."""
    @staticmethod
    def create(handler_type: str = "gpt", **kwargs) -> ModelInterface:
        """Create and return appropriate model handler."""
        handlers = {
            "gpt": lambda: GPTModelHandler(
                api_key=kwargs.get('api_key'),
                model=kwargs.get('model', 'gpt-4')
            ),
            "spacy": lambda: SpacyModelHandler(model_path=kwargs.get('model_path'))
        }

        if handler_type not in handlers:
            raise ValueError(f"Unknown handler type: {handler_type}")

        if handler_type == "spacy":
            logger.warning("Using deprecated Spacy model handler")

        return handlers[handler_type]()
