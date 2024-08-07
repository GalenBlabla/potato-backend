from fastapi import APIRouter, Depends
from typing import List

from app.models.notice_models import Announcement
from app.models.video_service_models import HtmlContentRequest, YearItem, TotalPages
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
    return await home_service.get_page_total_videos(decoded_content)


@router.get("/announcements", response_model=List[Announcement])
async def get_announcements(home_service: HomeService = Depends()):
    return home_service.get_announcements()


@router.post("/get_page_total_videos", response_model=List[VideoItem])
async def get_page_total_videos(request: HtmlContentRequest, home_service: HomeService = Depends()):
    decoded_content = decode_and_decompress(request.html_content)
    return await home_service.get_page_total_videos(decoded_content)


@router.post("/total_pages", response_model=TotalPages)
async def get_total_pages(request: HtmlContentRequest, home_service: HomeService = Depends()):
    decoded_content = decode_and_decompress(request.html_content)
    total_pages = await home_service.get_total_pages(decoded_content)
    return total_pages


@router.post("/years", response_model=List[YearItem])
async def extract_year_list(request: HtmlContentRequest, home_service: HomeService = Depends()):
    decoded_content = decode_and_decompress(request.html_content)
    year_list = await home_service.extract_year_list(decoded_content)
    return year_list
