# apptest/test.py
from fastapi.testclient import TestClient
from main import app

# 初始化测试客户端
client = TestClient(app)

def test_search():
    # 测试 /search/ 路由
    response = client.get("/api/search/search_kw/狐妖")
    assert response.status_code == 200
    assert response.json() is not None

def test_video_info():
    # 测试 /video_info/ 路由
    link = "/video/8955.html"
    response = client.get(f"/api/video_info/detail_page/?link={link}")
    assert response.status_code == 200
    assert "title" in response.json()

def test_episode_info():
    # 测试 /episode_info/ 路由
    episode_link = "https://www.dmla7.com/play/12-1-1.html"
    response = client.get(f"/api/episodes/episode_info/?episode_link={episode_link}")
    assert response.status_code == 200
    assert "video_source" in response.json()

def test_get_decrypted_url():
    # 测试 /get_decrypted_url/ 路由
    video_source = "https://danmu.yhdmjx.com/m3u8.php?url=%2FYotmSEeGwhHysjeQ%2FJwZYQadDItnoXPEhblEA8clOf6kEHPojbOwNAZFJz%2BXHyb"
    response = client.get(f"/api/episodes/get_decrypted_url/?video_source={video_source}")
    assert response.status_code == 200
    assert "decrypted_url" in response.json()
