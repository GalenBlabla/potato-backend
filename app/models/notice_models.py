# app/models/models.py
from pydantic import BaseModel
from typing import Optional


class Announcement(BaseModel):
    title: str
    content: str
    date: Optional[str] = None  # 可选字段，自动生成时间
