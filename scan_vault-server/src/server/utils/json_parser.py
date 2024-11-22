import json
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class JSONParser:
    """Utility class for parsing and validating JSON responses."""
    
    def parse_gpt_response(self, response: str) -> Dict:
        """Parse and validate GPT response."""
        try:
            json_content = self._extract_json_content(response)
            result = json.loads(json_content)
            return self._validate_and_fix_structure(result)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GPT response: {e}")
            return self._get_empty_result()

    def _extract_json_content(self, response: str) -> str:
        """Extract JSON content from response string."""
        if "```json" in response:
            return response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            return response.split("```")[1].strip()
        return response.strip()

    def _validate_and_fix_structure(self, result: Dict) -> Dict:
        """Validate and fix the structure of parsed JSON."""
        expected_keys = ['pii', 'phi', 'pci']
        for key in expected_keys:
            if key not in result:
                result[key] = []
        return result

    def _get_empty_result(self) -> Dict:
        """Return empty result structure."""
        return {"pii": [], "phi": [], "pci": []} 