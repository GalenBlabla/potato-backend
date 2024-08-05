import re
from bs4 import BeautifulSoup
from typing import List, Dict


class HomeInfoParser:

    def parse_carousel_videos(self, soup: BeautifulSoup) -> List[Dict]:
        """
        解析首页滚动条中的视频信息。
        :param soup: 首页的 BeautifulSoup 对象。
        :return: 包含视频信息（标题、图片和链接）的字典列表。
        """
        videos = []
        try:
            # 查找滚动条容器
            carousel = soup.find('div', class_='carousel')
            if not carousel:
                raise ValueError("未在首页找到滚动条。")

            # 获取滚动条中的每个视频项
            video_items = carousel.find_all('div', class_='list')
            for item in video_items:
                title = item.find('a', class_='stui-vodlist__thumb')['title']
                link = item.find('a', class_='stui-vodlist__thumb')['href']
                image_style = item.find('a', class_='stui-vodlist__thumb')['style']

                # 提取背景图片的 URL
                image_url = None
                match = re.search(r'url\((.*?)\)', image_style)
                if match:
                    image_url = match.group(1).strip("'\"")

                videos.append({
                    'title': title,
                    'link': link,
                    'image': image_url
                })
        except Exception as e:
            print(f"解析滚动条视频失败: {str(e)}")
            raise e

        return videos

    def parse_recommended_videos(self, soup: BeautifulSoup) -> List[Dict]:
        """
        解析首页推荐列表中的视频信息。每12个一组
        :param soup: BeautifulSoup 对象的首页内容。
        :return: 包含视频信息（标题、链接、图片、简介）的字典列表。
        """
        videos = []

        try:
            videos += self._parse_video_list(soup)
        except Exception as e:
            print(f"解析热播动漫推荐列表失败: {str(e)}")
            raise e

        return videos

    def _parse_video_list(self, section: BeautifulSoup) -> List[Dict]:
        """
        解析给定推荐列表中的视频信息。
        :param section: 推荐列表的 BeautifulSoup 对象。
        :return: 包含视频信息（标题、链接、图片、简介）的字典列表。
        """
        videos = []
        try:
            # 查找所有的li元素，每个li表示一个视频项
            video_items = section.find_all('li', class_='col-md-6')

            for item in video_items:
                title_tag = item.find('a', class_='stui-vodlist__thumb')
                detail_tag = item.find('div', class_='stui-vodlist__detail')
                # 获取标题和链接
                title = title_tag['title']
                link = title_tag['href']
                # 获取图片URL
                image = title_tag['data-original']
                # 获取简介
                description = detail_tag.find('p', class_='text text-overflow text-muted hidden-xs').get_text(
                    strip=True)

                videos.append({
                    'title': title,
                    'link': link,
                    'image': image,
                    'description': description
                })
        except Exception as e:
            print(f"解析视频列表失败: {str(e)}")
            raise e

        return videos
