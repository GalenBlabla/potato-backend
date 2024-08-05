from fastapi import APIRouter
from app.api import search, video_info, episodes, home

router = APIRouter()

# 注册各个子路由，并传入共享的 Service 实例
router.include_router(
    search.router, prefix="/search", tags=["Search"]
)
router.include_router(
    video_info.router, prefix="/video_info", tags=["Video Info"]
)
router.include_router(
    episodes.router, prefix="/episodes", tags=["Episodes"]
)
router.include_router(
    home.router, prefix="/home", tags=["Home"]
)
