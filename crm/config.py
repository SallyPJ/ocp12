import os
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Access environment variables
SECRET_KEY = os.getenv("JWT_SECRET")
REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

ACCESS_TOKEN_EXPIRES_IN = 600  # 10 minutes
REFRESH_TOKEN_EXPIRES_IN = 86400  # 24 hours

# 📌 Intégration of Sentry with SQLAlchemy and Logging
sentry_sdk.init(
    dsn="SENTRY_DSN",
    traces_sample_rate=1.0,  # Activate performance monitoring
    profiles_sample_rate=1.0,  # Activate profiling
    integrations=[
        LoggingIntegration(level="INFO", event_level="ERROR"),  # Capture des logs
        SqlalchemyIntegration(),  # Capture SQL requests
    ],
)
