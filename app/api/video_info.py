from fastapi import APIRouter, Depends
from app.models.video_service_models import VideoInfo, HtmlContentRequest
from app.scrapy.video_service import VideoService
from .utils.decode_and_decompress import decode_and_decompress


router = APIRouter()


@router.post("/detail_page", response_model=VideoInfo)
async def video_info(request: HtmlContentRequest, scraper: VideoService = Depends()):
    decoded_content = decode_and_decompress(request.html_content)
    info = await scraper.get_video_info(decoded_content)
    return info
