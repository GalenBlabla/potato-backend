import asyncio
from datetime import datetime

from bs4 import BeautifulSoup
from typing import List
from fastapi import HTTPException

from app.models.notice_models import Announcement
from app.scrapy.utils.http_client import HttpClient
from app.scrapy.utils.home_info_parser import HomeInfoParser
from app.models.home_service_models import VideoItem


class HomeService:
    def __init__(self):
        self.BASE_URL = "https://www.dmla7.com"
        self.http_client = HttpClient()
        self.home_info_parser = HomeInfoParser(self.BASE_URL)
        self.announcements = [
            Announcement(
                title="系统维护公告",
                content="系统将于2024年8月10日凌晨2点进行维护，期间服务将暂停期间服务将暂停期间服务将暂停期间服务将暂停期间服务将暂停期间服务将暂停期间服务将暂停期间服务将暂停。",
                date="2024-08-09"
            ),
            Announcement(
                title="系统维护公告",
                content="系统将于2024年8月10日凌晨2点进行维护，期间服务将暂停。",
                date="2024-08-09"
            ),
            Announcement(
                title="系统维护公告",
                content="系统将于2024年8月10日凌晨2点进行维护，期间服务将暂停。",
                date="2024-08-09"
            ),
            Announcement(
                title="系统维护公告",
                content="系统将于2024年8月10日凌晨2点进行维护，期间服务将暂停。",
                date="2024-08-09"
            ),
            Announcement(
                title="新功能上线",
                content="我们新增了多个精彩的功能，欢迎体验！",
                date="2024-08-01"
            )


        ]

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

    def get_announcements(self) -> List[Announcement]:
        return self.announcements
# 测试代码
async def main():
    home_service = HomeService()

    try:
        # 获取首页滚动条视频
        carousel_videos = await home_service.get_carousel_videos()
        print("滚动条视频：",carousel_videos)


        # 获取热播动漫推荐列表
        recommended_videos = await home_service.get_recommended_videos()
        print("\n热播动漫推荐：",recommended_videos)

    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())
