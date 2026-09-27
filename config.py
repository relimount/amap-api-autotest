import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

AMAP_KEY = os.getenv("AMAP_KEY")
BASE_URL = "https://restapi.amap.com/"
TIMEOUT = 10

PROJECT_ROOT = Path(__file__).resolve().parent
