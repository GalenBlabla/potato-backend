from fastapi import APIRouter, Depends
from app.models.video_service_models import VideoItem, HtmlContentRequest
from app.scrapy.video_service import VideoService
from typing import List
from .utils.decode_and_decompress import decode_and_decompress

router = APIRouter()


@router.post("/search_kw", response_model=List[VideoItem])
async def search(request: HtmlContentRequest, scraper: VideoService = Depends()):
    decoded_content = decode_and_decompress(request.html_content)
    return await scraper.search(decoded_content)
