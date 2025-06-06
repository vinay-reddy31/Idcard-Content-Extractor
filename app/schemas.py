from pydantic import BaseModel
from typing import Dict, List, Optional

class ExtractRequest(BaseModel):
    image_base64: str

class ExtractResponse(BaseModel):
    user_id: str
    extracted_fields: Dict[str, str]
    confidence_score: float
    missing_fields: List[str]
    status: str