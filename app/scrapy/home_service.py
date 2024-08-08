from bs4 import BeautifulSoup
from typing import List, Dict

from app.models.notice_models import Announcement
from app.scrapy.utils.home_info_parser import HomeInfoParser
from app.models.home_service_models import VideoItem


class HomeService:
    def __init__(self):
        self.home_info_parser = HomeInfoParser()
        self.announcements = [
            Announcement(
                title="公告：本项目已开源",
                content="开源地址：https://github.com/GalenBlabla/potato，可自行访问并下载最新发布版本！",
                date="2024-08-09"
            ),
            Announcement(
                title="公告：当前软件存在已知问题",
                content="切换视频不要过快，当一个视频还没有加载出画面的时候立马切换到下一个视频或者退出当前页面，该视频会变成僵尸视频一直在后台播放。退出软件才能关。"
                        "资源页面的翻页还没那么丝滑。",
                date="2024-08-09"
            ),
            Announcement(
                title="公告：当前软件存在恶意代码/病毒",
                content="应用权限问题：当前软件没有向手机申请任何权限，不涉及任何隐私",
                date="2024-08-09"
            ),

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

    async def get_page_total_videos(self, html_content: str) -> List[VideoItem]:
        soup = await self.parse_homepage(html_content)
        video_data = self.home_info_parser.parse_page_total_videos(soup)
        return [VideoItem(**video) for video in video_data]

    def get_announcements(self) -> List[Announcement]:
        return self.announcements

    async def get_total_pages(self, html_content: str) -> dict:
        soup = await self.parse_homepage(html_content)
        return self.home_info_parser.get_total_pages(soup)

    async def extract_year_list(self, html_content: str) -> List[Dict]:
        soup = await self.parse_homepage(html_content)
        return self.home_info_parser.extract_year_list(soup)
