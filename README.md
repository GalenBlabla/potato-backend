# Potato-Backend 爬虫后端

**Potato-Backend** 服务于[Potato](https://github.com/GalenBlabla/Potato) ，是一个采用分布式爬虫思想的项目，旨在实现高效的网页数据抓取。该项目的后端部分主要负责处理前端传送的 HTML 数据，而爬虫的请求是由客户端直接发送。

## 主要特点

- **分布式爬虫**：后端处理前端传送的 HTML 数据，这样可以减轻后端服务器的压力，并且更灵活地进行数据抓取。
- **基于 FastAPI 和 Pydantic**：使用 FastAPI 作为后端框架，结合 Pydantic 进行数据验证，确保高效和安全的数据处理。
- **无缓存和数据库**：当前版本没有使用任何缓存机制和数据库，适合快速部署和测试。


## 快速开始

按照以下步骤克隆并运行 Potato 爬虫后端：

1. 克隆代码仓库

    ```bash
    git clone https://github.com/GalenBlabla/Potato-Backend.git
    ```

2. 进入项目目录

    ```bash
    cd Potato-Backend
    ```

3. 安装依赖

    ```bash
    pip install -r requirements.txt
    ```

4. 运行主程序

    ```bash
    python main.py
    ```

## 使用方法

### 启动后端服务

在启动后端服务后，您可以通过浏览器访问 `http://localhost:8001/docs` 来测试 API 接口。

### 前端发送 HTML 数据

前端可以通过 HTTP POST 请求将抓取到的 HTML 数据发送到后端指定的 API 接口进行处理。后端会解析并处理这些数据，然后返回结果。


