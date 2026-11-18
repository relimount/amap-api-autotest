import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

AMAP_KEY = os.getenv("AMAP_KEY")
if not AMAP_KEY:
    raise RuntimeError("AMAP_KEY 未配置：请在项目根目录创建 .env 或设置环境变量")

ENVIRONMENT = {
    "prod": "https://restapi.amap.com/",
    "mock": "http://127.0.0.1:8000/",
}
BASE_URL = ENVIRONMENT["prod"]

TIMEOUT = 10

PROJECT_ROOT = Path(__file__).resolve().parent
