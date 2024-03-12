from app import create_app, db
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app(os.getenv("FLASK_CONFIG") or 'default')