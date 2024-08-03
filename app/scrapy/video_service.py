import re
import aiohttp
from app.scrapy.utils.http_client import HttpClient
from app.scrapy.utils.video_info_parser import VideoInfoParser
from app.scrapy.utils.decryptor import Decryptor
from typing import List, Dict

from fastapi import HTTPException


class VideoService:
    def __init__(self):
        self.BASE_URL = "https://www.dmla7.com"
        self.http_client = HttpClient()
        self.video_info_parser = VideoInfoParser(self.BASE_URL)
        self.decryptor = Decryptor()

    async def search(self, query: str) -> List[Dict]:
        url = f"{self.BASE_URL}/search/-------------.html?wd={query}"
        soup = await self.http_client.get_soup(url)
        return self.video_info_parser.parse_video_list(soup)

    async def get_video_info(self, link: str) -> Dict:
        soup = await self.http_client.get_soup(self.BASE_URL + link)
        return self.video_info_parser.parse_video_info(soup)

    async def get_episode_info(self, episode_link: str) -> str:
        soup = await self.http_client.get_soup(episode_link)
        return self.video_info_parser.parse_episode_link(soup)

    async def get_decrypted_url(self, video_source: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(video_source) as source_response:
                if source_response.status == 200:
                    text = await source_response.text()
                    video_info_params = self.extract_get_video_info_params(text)
                    if video_info_params:
                        video_url = video_info_params[0]
                        return self.decryptor.decrypt(video_url)
                    else:
                        raise HTTPException(status_code=404, detail="No video info parameters found in the response.")
                else:
                    if source_response.status == 404:
                        raise HTTPException(status_code=404,
                                            detail="The provided video link may have expired. Please try to get a new link.")
                    else:
                        raise HTTPException(status_code=source_response.status,
                                            detail="Failed to retrieve the video source")

    @staticmethod
    def extract_get_video_info_params(response_text: str) -> List[str]:
        pattern = r'getVideoInfo\("([^"]+)"\)'
        matches = re.findall(pattern, response_text)
        return matches
