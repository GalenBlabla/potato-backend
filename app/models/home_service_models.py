from pydantic import BaseModel
from typing import Optional


class VideoItem(BaseModel):
    title: str
    link: str
    image: str
    description: Optional[str] = None
