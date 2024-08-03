import asyncio
from bs4 import BeautifulSoup
from typing import List
from fastapi import HTTPException
from app.scrapy.utils.http_client import HttpClient
from app.scrapy.utils.home_info_parser import HomeInfoParser
from app.models.home_service_models import VideoItem


class HomeService:
    def __init__(self):
        self.BASE_URL = "https://www.dmla7.com"
        self.http_client = HttpClient()
        self.home_info_parser = HomeInfoParser(self.BASE_URL)

    async def fetch_homepage(self) -> BeautifulSoup:
        homepage_url = self.BASE_URL
        try:
            soup = await self.http_client.get_soup(homepage_url)
            return soup
        except HTTPException as e:
            print(f"获取首页失败: {e.detail}")
            raise e

    async def get_carousel_videos(self) -> List[VideoItem]:
        soup = await self.fetch_homepage()
        video_data = self.home_info_parser.parse_carousel_videos(soup)
        return [VideoItem(**video) for video in video_data]

    async def get_recommended_videos(self) -> List[VideoItem]:
        soup = await self.fetch_homepage()
        video_data = self.home_info_parser.parse_recommended_videos(soup)
        return [VideoItem(**video) for video in video_data]


# 测试代码
# async def main():
#     home_service = HomeService()
#
#     try:
#         # 获取首页滚动条视频
#         carousel_videos = await home_service.get_carousel_videos()
#         print("滚动条视频：",carousel_videos)
#
#
#         # 获取热播动漫推荐列表
#         recommended_videos = await home_service.get_recommended_videos()
#         print("\n热播动漫推荐：",recommended_videos)
#
#     except Exception as e:
#         print(f"发生错误: {e}")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
