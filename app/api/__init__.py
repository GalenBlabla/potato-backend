from fastapi import APIRouter, Depends
from app.api import search, video_info, episodes, home
from app.scrapy.video_service import VideoService
from app.scrapy.home_service import HomeService

router = APIRouter()
video_service = VideoService()
home_service = HomeService()


# 依赖注入：所有路由共享一个 VideoService 实例
def get_video_service():
    return video_service


# 依赖注入：所有路由共享一个 HomeService 实例
def get_home_service():
    return home_service


# 注册各个子路由，并传入共享的 Service 实例
router.include_router(
    search.router, prefix="/search", tags=["Search"], dependencies=[Depends(get_video_service)]
)
router.include_router(
    video_info.router, prefix="/video_info", tags=["Video Info"], dependencies=[Depends(get_video_service)]
)
router.include_router(
    episodes.router, prefix="/episodes", tags=["Episodes"], dependencies=[Depends(get_video_service)]
)
router.include_router(
    home.router, prefix="/home", tags=["Home"], dependencies=[Depends(get_home_service)]
)
router.include_router(
    home.router, prefix="/home", tags=["Home"], dependencies=[Depends(get_home_service)]
)