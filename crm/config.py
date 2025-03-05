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

# 📌 Intégration de Sentry avec SQLAlchemy et Logging
sentry_sdk.init(
    dsn="https://59fa82cbee5bf596c98f22c1a22b456c@o4508876971769856.ingest.de.sentry.io/4508876976029776",
    traces_sample_rate=1.0,  # Active la capture des performances
    profiles_sample_rate=1.0,  # Active le profiling
    integrations=[
        LoggingIntegration(level="INFO", event_level="ERROR"),  # Capture des logs
        SqlalchemyIntegration()  # Capture des requêtes SQL
    ]
)
