# app/api/video_info.py
from fastapi import APIRouter, Depends
from app.models.video_service_models import VideoInfo
from app.scrapy.video_service import VideoService

router = APIRouter()


@router.get("/detail_page/", response_model=VideoInfo)
async def video_info(link: str, scraper: VideoService = Depends()):
    info = await scraper.get_video_info(link)
    return info
