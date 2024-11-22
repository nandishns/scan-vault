from fastapi import File
from pydantic import BaseModel
from fastapi import UploadFile

class ScanRequest(BaseModel):
    file: UploadFile = File(...)

