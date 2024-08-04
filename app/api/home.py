from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.models.notice_models import Announcement
from app.scrapy.home_service import HomeService, VideoItem

router = APIRouter()


# 使用 Depends 注入 HomeService 实例
@router.get("/carousel_videos", response_model=List[VideoItem])
async def get_carousel_videos(home_service: HomeService = Depends()):
    return await home_service.get_carousel_videos()


@router.get("/recommended_videos", response_model=List[VideoItem])
async def get_recommended_videos(home_service: HomeService = Depends()):
    return await home_service.get_recommended_videos()


@router.get("/announcements", response_model=List[Announcement])
async def get_announcements(home_service: HomeService = Depends()):
    return home_service.get_announcements()