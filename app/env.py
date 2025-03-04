import os

BASE_URL = os.getenv("BASE_URL")

if BASE_URL is None:
    BASE_URL = "http://127.0.0.1:8000"