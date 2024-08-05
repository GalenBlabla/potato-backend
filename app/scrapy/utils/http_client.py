import aiohttp
from bs4 import BeautifulSoup
from fastapi import HTTPException


class HttpClient:
    async def get_soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')
