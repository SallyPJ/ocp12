import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Access environment variables
SECRET_KEY = os.getenv("JWT_SECRET")
REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")
