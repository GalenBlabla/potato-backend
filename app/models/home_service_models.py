from pydantic import BaseModel, Field
from typing import Optional



class VideoItem(BaseModel):
    title: str = Field(..., description="视频标题")
    link: str = Field(..., description="视频链接")
    image: Optional[str] = Field(None, description="视频缩略图URL")
    description: Optional[str] = Field(None, description="视频描述")



