# File: app/db/supabase.py
from supabase import create_client, Client
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("TAP.Database")

try:
    logger.info("Initializing Supabase Client...")
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    logger.info("Supabase Client initialized.")
except Exception as e:
    logger.critical(f"FAILED to initialize Supabase: {str(e)}", exc_info=True)
    raise e