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
        self.home_info_parser = HomeInfoParser()
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

    async def parse_homepage(self, html_content: str) -> BeautifulSoup:
        """
        解析客户端传递的HTML内容并返回BeautifulSoup对象。
        :param html_content: HTML内容字符串
        :return: BeautifulSoup对象
        """
        return BeautifulSoup(html_content, 'html.parser')

    async def get_carousel_videos(self, html_content: str) -> List[VideoItem]:
        soup = await self.parse_homepage(html_content)
        video_data = self.home_info_parser.parse_carousel_videos(soup)
        return [VideoItem(**video) for video in video_data]

    async def get_recommended_videos(self, html_content: str) -> List[VideoItem]:
        soup = await self.parse_homepage(html_content)
        video_data = self.home_info_parser.parse_recommended_videos(soup)
        return [VideoItem(**video) for video in video_data]

    def get_announcements(self) -> List[Announcement]:
        return self.announcements
