# settings.py
from dotenv import load_dotenv
load_dotenv()
import os

class Config:
    access_tokne = os.getenv("access_tokne")
    access_token_secret = os.getenv("access_token_secret")
    consumer_key = os.getenv("consumer_key")
    consumer_secret = os.getenv("consumer_secret")

    es_hosts = os.getenv("es_hosts").split(',')
    es_http_user = os.getenv("es_http_user")
    es_http_pwd = os.getenv("es_http_pwd")