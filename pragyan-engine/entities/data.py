from pydantic import BaseModel
from fastapi import UploadFile


class ExtractData(BaseModel):
    extract_name: str
    engine_id: str
    query_str: str


class UploadData(BaseModel):
    extract_name: str
    file_type: str
