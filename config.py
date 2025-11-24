from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("URL")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")