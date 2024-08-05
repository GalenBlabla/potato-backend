import re
import aiohttp
from bs4 import BeautifulSoup

from app.scrapy.utils.video_info_parser import VideoInfoParser
from app.scrapy.utils.decryptor import Decryptor
from typing import List, Dict

from fastapi import HTTPException


class VideoService:
    def __init__(self):
        self.video_info_parser = VideoInfoParser()
        self.decryptor = Decryptor()

    async def parse_video_page(self, html_content: str) -> BeautifulSoup:
        """
        解析客户端传递的HTML内容并返回BeautifulSoup对象。
        :param html_content: HTML内容字符串
        :return: BeautifulSoup对象
        """
        return BeautifulSoup(html_content, 'html.parser')

    async def search(self, html_content: str) -> List[Dict]:
        soup = await self.parse_video_page(html_content)
        # print("soup", soup)
        return self.video_info_parser.parse_video_list(soup)

    async def get_video_info(self, html_content: str) -> Dict:
        soup = await self.parse_video_page(html_content)
        return self.video_info_parser.parse_video_info(soup)

    async def get_episode_info(self, html_content: str) -> str:
        soup = await self.parse_video_page(html_content)
        return self.video_info_parser.parse_episode_link(soup)

    async def get_decrypted_url(self, html_content: str) -> str:
        video_info_params = self.extract_get_video_info_params(html_content)
        if video_info_params:
            video_url = video_info_params[0]
            return self.decryptor.decrypt(video_url)
        else:
            raise HTTPException(status_code=404, detail="No video info parameters found in the response.")

    @staticmethod
    def extract_get_video_info_params(response_text: str) -> List[str]:
        pattern = r'getVideoInfo\("([^"]+)"\)'
        matches = re.findall(pattern, response_text)
        return matches
