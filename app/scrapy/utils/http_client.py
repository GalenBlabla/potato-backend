import aiohttp
from bs4 import BeautifulSoup
from fastapi import HTTPException


class HttpClient:
    async def fetch(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise HTTPException(status_code=response.status, detail=f"Failed to retrieve the webpage at {url}")

    async def get_soup(self, url: str) -> BeautifulSoup:
        html = await self.fetch(url)
        return BeautifulSoup(html, 'html.parser')
