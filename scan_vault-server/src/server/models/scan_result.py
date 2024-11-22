from typing import List, Dict, Union
from pydantic import BaseModel

class SensitiveField(BaseModel):
    field_name: str
    value: str
    category: str  # PII, PHI, PCI

class ScanResult(BaseModel):
    file_name: str
    sensitive_fields: List[SensitiveField]
    summary: Dict[str, int]  # Count of each sensitive data type
