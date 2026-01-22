"""
Application.config
Handles configuration loading from environment variables and Resource Path resolution
"""

import os
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import logging

logger = logging.getLogger(__name__)

#* Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logger.warning("python-dotenv not installed. Using environment variables directly.")


def get_resource_path(relative_path):
    """ 
    Get absolute path to resource, works for dev and for PyInstaller.
    
    Args:
        relative_path (str): The path relative to the Application folder. 
                             Example: 'GUI/UI/home_screen.ui' (Do NOT include 'Application/')
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


def load_env_file():
    """
    Load environment variables from .env file
    Checks PyInstaller bundle first, then local directories.
    """
    internal_env = Path(get_resource_path('.env'))
    
    if getattr(sys, 'frozen', False):
        external_env = Path(sys.executable).parent / '.env'
    else:
        external_env = Path(__file__).resolve().parent.parent / '.env'

    env_file = None
    
    if internal_env.exists():
        env_file = internal_env
    elif external_env.exists():
        env_file = external_env
    
    if env_file and DOTENV_AVAILABLE:
        load_dotenv(env_file)
        logger.info(f"Loaded .env file from: {env_file}")
        return True
    elif env_file:
        logger.warning(f".env found at {env_file} but python-dotenv is missing.")
        return False
    else:
        logger.info("No .env file found. Using environment variables.")
        return False


def get_database_config():
    """
    Get database configuration from environment variables
    Returns a dictionary with database connection parameters
    """
    #* Load .env file if available
    load_env_file()
    
    #* Get database URI from environment variable
    neon_uri = os.getenv("DATABASE_URL") or os.getenv("NEON_URI")
    
    if not neon_uri:
        logger.error("DATABASE_URL or NEON_URI environment variable not found!")
        raise ValueError(
            "Database connection string not found. "
            "Ensure .env is in the same folder as the executable or bundled correctly."
        )
    
    #* Parse the URI
    try:
        parsed = urlparse(neon_uri)
        query_params = parse_qs(parsed.query)
        
        config = {
            "database": parsed.path.lstrip('/'),
            "user": parsed.username,
            "password": parsed.password,
            "host": parsed.hostname,
            "port": str(parsed.port) if parsed.port else "5432",
            "sslmode": query_params.get('sslmode', ['require'])[0],
            "channel_binding": query_params.get('channel_binding', ['require'])[0] if 'channel_binding' in query_params else None
        }
        
        #* Remove None values
        config = {k: v for k, v in config.items() if v is not None}
        
        logger.info(f"Database config loaded for host: {config['host']}")
        return config
        
    except Exception as e:
        logger.error(f"Error parsing database URI: {e}")
        raise ValueError(f"Invalid database connection string: {e}")