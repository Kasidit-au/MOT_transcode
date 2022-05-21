# settings.py
from dotenv import load_dotenv
load_dotenv()
import os

class Config:
    es_hosts = os.getenv("es_hosts").split(',')
    es_http_user = os.getenv("es_http_user")
    es_http_pwd = os.getenv("es_http_pwd")
