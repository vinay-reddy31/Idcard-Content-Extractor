from pydantic import BaseModel

class ExtractRequest(BaseModel):
    image_base64: str

class ExtractResponse(BaseModel):
    status: str
    extracted_fields: dict