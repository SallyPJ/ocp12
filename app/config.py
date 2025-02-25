import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Access environment variables
SECRET_KEY = os.getenv("JWT_SECRET")
REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

ACCESS_TOKEN_EXPIRES_IN = 600 # 10 minutes
REFRESH_TOKEN_EXPIRES_IN = 86400 # 24 hours