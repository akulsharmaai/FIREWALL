import logging
import sys
from app.core.config import settings

def setup_logging():
    """Configure basic logging for the backend."""
    
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Suppress verbose loggers if needed
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

logger = logging.getLogger("human_firewall")
