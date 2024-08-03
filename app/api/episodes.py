# app/api/episodes.py
from fastapi import APIRouter, Depends
from app.models.video_service_models import EpisodeInfoResponse, DecryptedURLResponse
from app.scrapy.video_service import VideoService

router = APIRouter()


@router.get("/episode_info/", response_model=EpisodeInfoResponse)
async def episode_info(episode_link: str, scraper: VideoService = Depends()):
    video_source = await scraper.get_episode_info(episode_link)
    return {"video_source": video_source}


@router.get("/get_decrypted_url/", response_model=DecryptedURLResponse)
async def get_decrypted_url(video_source: str, scraper: VideoService = Depends()):
    decrypted_url = await scraper.get_decrypted_url(video_source)
    return {"decrypted_url": decrypted_url}
