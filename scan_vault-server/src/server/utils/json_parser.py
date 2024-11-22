import json
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class JSONParser:
    """Utility class for parsing and validating JSON responses."""
    
    def parse_gpt_response(self, response: str) -> Dict:
        """Parse and validate GPT response."""
        try:
            # Clean the response string
            json_content = self._extract_json_content(response)
            
            # Parse JSON
            result = json.loads(json_content)
            
            # Convert flat array to categorized structure
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GPT response: {e}")
            logger.debug(f"Problematic response: {response}")
            return self._get_empty_result()

    def _extract_json_content(self, response: str) -> str:
        """Extract JSON content from response string."""
        try:
            # Remove any markdown code blocks
            if "```json" in response:
                content = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                content = response.split("```")[1].split("```")[0]
            else:
                content = response
            
            # Clean the string
            content = content.strip()
            
            # Find the first '[' and last ']'
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end != 0:
                content = content[start:end]
                
            return content
            
        except Exception as e:
            logger.error(f"Error extracting JSON content: {e}")
            return response.strip()

    def _categorize_results(self, results: list) -> Dict:
        """Organize flat array results into categories."""
        categorized = {
            "pii": [],
            "phi": [],
            "pci": []
        }
        
        for item in results:
            if isinstance(item, dict) and "category" in item:
                category = item["category"].lower()
                if category in categorized:
                    # Remove the category field since it's now implicit
                    item_copy = item.copy()
                    item_copy.pop("category", None)
                    categorized[category].append(item_copy)
        
        return categorized

    def _get_empty_result(self) -> Dict:
        """Return empty result structure."""
        return {"pii": [], "phi": [], "pci": []} 