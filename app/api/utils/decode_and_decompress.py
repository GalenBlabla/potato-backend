# app/api/utils.py
import base64
import gzip
from fastapi import HTTPException


def decode_and_decompress(content: str) -> str:
    try:
        compressed_content = base64.b64decode(content)
        return gzip.decompress(compressed_content).decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {str(e)}")
