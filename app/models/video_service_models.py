# app/video_service_models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class VideoItem(BaseModel):
    title: str = Field(default="N/A", description="The title of the video")
    link: str = Field(default="N/A", description="The link to the video page")
    alias: Optional[str] = Field(default="N/A", description="The alias of the video")
    actors: Optional[str] = Field(default="N/A", description="Actors in the video")
    genre: Optional[str] = Field(default="N/A", description="The genre of the video")
    region: Optional[str] = Field(default="N/A", description="The region of the video")
    year: Optional[str] = Field(default="N/A", description="The year of release")
    thumbnail: Optional[str] = Field(default="N/A", description="Thumbnail image URL")


class HtmlContentRequest(BaseModel):
    html_content: str


class Episode(BaseModel):
    name: str
    url: str


class VideoInfo(BaseModel):
    title: str
    alias: Optional[str]
    actors: Optional[str]
    genre: Optional[str]
    region: Optional[str]
    year: Optional[str]
    update: Optional[str]
    description: Optional[str]
    episodes: Dict[str, List[Episode]]


class DecryptedURLResponse(BaseModel):
    decrypted_url: str


class EpisodeInfoResponse(BaseModel):
    video_source: str


class YearItem(BaseModel):
    year: str = Field(..., description="年份")
    link: str = Field(..., description="该年份视频的链接")


class TotalPages(BaseModel):
    total_pages: int = Field(..., description="总页数")
