# app/api/__init__.py
from fastapi import APIRouter, Depends
from app.api import search, video_info, episodes
from app.scrapy.video_service import VideoService

router = APIRouter()
video_service = VideoService()


# 依赖注入：所有路由共享一个 VideoService 实例
def get_video_service():
    return video_service


# 注册各个子路由，并传入共享的 VideoService 实例
router.include_router(
    search.router, prefix="/search", tags=["Search"], dependencies=[Depends(get_video_service)]
)
router.include_router(
    video_info.router, prefix="/video_info", tags=["Video Info"], dependencies=[Depends(get_video_service)]
)
router.include_router(
    episodes.router, prefix="/episodes", tags=["Episodes"], dependencies=[Depends(get_video_service)]
)
