from fastapi import APIRouter, Depends
from app.models.video_service_models import EpisodeInfoResponse, DecryptedURLResponse, HtmlContentRequest
from app.scrapy.video_service import VideoService
from .utils.decode_and_decompress import decode_and_decompress


router = APIRouter()


@router.post("/episode_info", response_model=EpisodeInfoResponse)
async def episode_info(request: HtmlContentRequest, scraper: VideoService = Depends()):
    decoded_content = decode_and_decompress(request.html_content)
    video_source = await scraper.get_episode_info(decoded_content)
    return {"video_source": video_source}


@router.post("/get_decrypted_url", response_model=DecryptedURLResponse)
async def get_decrypted_url(request: HtmlContentRequest, scraper: VideoService = Depends()):
    decoded_content = decode_and_decompress(request.html_content)
    decrypted_url = await scraper.get_decrypted_url(decoded_content)
    return {"decrypted_url": decrypted_url}
