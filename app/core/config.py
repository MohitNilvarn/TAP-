# File: app/core/config.py
import os
from dotenv import load_dotenv
from app.core.logger import get_logger

# Note: We don't run setup_logging() here because main.py handles it.
# We just get a logger instance.
logger = get_logger("TAP.Config")

logger.info("Loading environment variables...")
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Teacher Assistance Platform"
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

    def __init__(self):
        if not self.SUPABASE_URL:
            logger.critical("MISSING ENV VAR: SUPABASE_URL")
        elif not self.SUPABASE_KEY:
            logger.critical("MISSING ENV VAR: SUPABASE_KEY")
        else:
            logger.info("Config loaded successfully.")

settings = Settings()