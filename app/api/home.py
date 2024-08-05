from fastapi import APIRouter, Depends
from typing import List

from app.models.notice_models import Announcement
from app.models.video_service_models import HtmlContentRequest
from app.scrapy.home_service import HomeService, VideoItem
from .utils.decode_and_decompress import decode_and_decompress

router = APIRouter()


# 使用 Depends 注入 HomeService 实例
@router.post("/carousel_videos", response_model=List[VideoItem])
async def get_carousel_videos(request: HtmlContentRequest, home_service: HomeService = Depends()):
    decoded_content = decode_and_decompress(request.html_content)
    return await home_service.get_carousel_videos(decoded_content)


@router.post("/recommended_videos", response_model=List[VideoItem])
async def get_recommended_videos(request: HtmlContentRequest, home_service: HomeService = Depends()):
    decoded_content = decode_and_decompress(request.html_content)
    return await home_service.get_recommended_videos(decoded_content)


@router.get("/announcements", response_model=List[Announcement])
async def get_announcements(home_service: HomeService = Depends()):
    return home_service.get_announcements()
