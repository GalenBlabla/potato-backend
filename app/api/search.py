# app/api/search.py
from fastapi import APIRouter, Depends
from app.models.video_service_models import VideoItem
from app.scrapy.video_service import VideoService
from typing import List

router = APIRouter()


@router.get("/search_kw/{query}", response_model=List[VideoItem])
async def search(query: str, scraper: VideoService = Depends()):
    results = await scraper.search(query)
    return results
