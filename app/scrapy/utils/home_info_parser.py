import re
from bs4 import BeautifulSoup
from typing import List, Dict


class HomeInfoParser:

    def parse_carousel_videos(self, html_content: BeautifulSoup) -> List[Dict]:
        """
        解析首页滚动条中的视频信息。
        """
        videos = []
        try:
            # 查找滚动条容器
            carousel = html_content.find('div', class_='carousel')
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

    def parse_page_total_videos(self, html_content: BeautifulSoup) -> List[Dict]:
        """
        解析首页推荐列表中的视频信息。每12个一组
        """
        videos = []

        try:
            videos += self._parse_video_list(html_content)
        except Exception as e:
            print(f"解析热播动漫推荐列表失败: {str(e)}")
            raise e

        return videos

    def _parse_video_list(self, html_content: BeautifulSoup) -> List[Dict]:
        """
        解析给定推荐列表中的视频信息。
        """
        videos = []
        try:
            # 查找所有的li元素，每个li表示一个视频项
            video_items = html_content.find_all('li', class_='col-md-6')

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

    def get_total_pages(self, html_content: BeautifulSoup) -> Dict:
        pagination = html_content.find('ul', class_='stui-page text-center clearfix')
        if not pagination:
            return {
                'total_pages': 'failed'
            }

        last_page_link = pagination.find_all('a')[-1]['href']
        match = re.search(r'-(\d+)', last_page_link)

        if match:
            return {
                'total_pages': int(match.group(1))
            }
        else:
            return {
                'total_pages': 'failed'
            }

    def extract_year_list(self, html_content: BeautifulSoup) -> List[Dict]:
        pannel_hd = html_content.find('div', class_='stui-pannel_hd')
        if not pannel_hd:
            raise ValueError("未找到 'stui-pannel_hd' 组件。")

        screen_lists = pannel_hd.find_all('ul', class_='stui-screen__list')
        year_list = []
        for screen_list in screen_lists:
            if screen_list.find('span', class_='text-muted') and '按年份' in screen_list.find('span',
                                                                                              'text-muted').text:
                for li in screen_list.find_all('li'):
                    a_tag = li.find('a')
                    if a_tag:
                        link = a_tag['href']
                        text = a_tag.get_text(strip=True)
                        year_list.append({'year': text, 'link': link})
                break

        return year_list
