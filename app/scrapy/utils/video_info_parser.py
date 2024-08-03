# app/scraper/video_info_parser.py
from bs4 import BeautifulSoup
from typing import List, Dict

from fastapi import HTTPException


class VideoInfoParser:
    def __init__(self, base_url: str):
        self.BASE_URL = base_url

    def parse_video_list(self, soup: BeautifulSoup) -> List[Dict]:
        parent_div = soup.find('div', class_='stui-pannel_bd')
        if not parent_div:
            raise HTTPException(status_code=404, detail="No search results found.")

        video_list = []
        results = parent_div.find_all('li')
        for item in results:
            video_list.append(self._parse_video_item(item))
        return video_list

    def _parse_video_item(self, item) -> Dict:
        title = item.find('h3', class_='title').get_text(strip=True) if item.find('h3', class_='title') else 'N/A'
        link = item.find('a', class_='v-thumb')['href'] if item.find('a', class_='v-thumb') else 'N/A'
        alias = self._get_next_sibling_text(item, 'span', '别名：', 'N/A').replace('别名：', '')
        actors = self._get_next_sibling_text(item, 'span', '主演：', 'N/A')
        genre = self._get_next_sibling_text(item, 'span', '类型：', 'N/A')
        region = self._get_next_sibling_text(item, 'span', '地区：', 'N/A')
        year = self._get_next_sibling_text(item, 'span', '年份：', 'N/A')
        thumbnail = item.find('a', class_='v-thumb')['data-original'] if item.find('a', class_='v-thumb') else 'N/A'
        return {
            'title': title,
            'link': link,
            'alias': alias,
            'actors': actors,
            'genre': genre,
            'region': region,
            'year': year,
            'thumbnail': thumbnail
        }

    def _get_next_sibling_text(self, item, tag_name: str, class_name: str, default: str) -> str:
        element = item.find(tag_name, string=class_name)
        if element and element.next_sibling:
            next_sibling = element.next_sibling
            return next_sibling.strip() if isinstance(next_sibling, str) else default
        return default

    def parse_video_info(self, soup: BeautifulSoup) -> Dict:
        title = soup.find('h1', class_='title').get_text(strip=True)
        alias = soup.find('p', class_='data').get_text(strip=True).replace('别名：', '') if soup.find('p',
                                                                                                     class_='data') else 'N/A'
        actors = ', '.join([a.get_text(strip=True) for a in soup.find_all('a', href=True) if 'search/' in a['href']])
        genre = soup.find('a', href=True).get_text(strip=True)
        region = self._get_next_sibling_text(soup, 'span', '地区：', 'N/A')
        year = self._get_next_sibling_text(soup, 'span', '年份：', 'N/A')
        update = soup.find('p', class_='data hidden-sm').get_text(strip=True) if soup.find('p',
                                                                                           'data hidden-sm') else 'N/A'
        description = soup.find('p', class_='desc hidden-xs').get_text(strip=True) if soup.find('p',
                                                                                                'desc hidden-xs') else 'N/A'
        episodes = self._extract_episodes(soup)
        return {
            'title': title,
            'alias': alias,
            'actors': actors,
            'genre': genre,
            'region': region,
            'year': year,
            'update': update,
            'description': description,
            'episodes': episodes
        }

    def _extract_episodes(self, soup: BeautifulSoup) -> Dict[str, List[Dict[str, str]]]:
        episodes = {}
        playlists = soup.find_all('div', class_='tab-pane fade in clearfix')
        for idx, playlist in enumerate(playlists, start=1):
            line_name = f"线路{idx}"
            episode_links = [{"name": a.get_text(strip=True), "url": f"{self.BASE_URL}{a['href']}"} for a in
                             playlist.find_all('a', href=True) if '/play/' in a['href']]
            episodes[line_name] = episode_links
        return episodes

    def parse_episode_link(self, soup: BeautifulSoup) -> str:
        iframe = soup.find('iframe', src=True)
        if iframe:
            return iframe['src']
        else:
            script = soup.find('script', string=lambda text: 'player_aaaa' in text if text else False)
            if script:
                encoded_url = self._extract_url_from_script(script.string)
                return f"https://danmu.yhdmjx.com/m3u8.php?url={encoded_url}"
        raise HTTPException(status_code=404, detail="Video source not found")

    def _extract_url_from_script(self, script_text: str) -> str:
        start = script_text.find('url":"') + 6
        end = script_text.find('","url_next')
        return script_text[start:end]
