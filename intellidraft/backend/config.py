"""
Configuration management for IntelliDraft backend
Loads environment variables from .env file
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # OpenRouter API (replaces OpenAI)
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    
    # Digi-Key (optional - can use hardcoded values in digikey.py for now)
    digikey_client_id: str = os.getenv("DIGIKEY_CLIENT_ID", "")
    digikey_client_secret: str = os.getenv("DIGIKEY_CLIENT_SECRET", "")
    
    # Paths
    library_path: Path = Path(__file__).parent.parent / "Library"
    upload_dir: Path = Path(__file__).parent / "uploads"
    output_dir: Path = Path(__file__).parent / "outputs"

settings = Settings()
