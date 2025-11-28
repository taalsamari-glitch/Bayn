from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # app/core -> app

class Settings(BaseSettings):
    AZURE_TTS_KEY: str
    AZURE_TTS_REGION: str
    AZURE_TTS_VOICE: str = "en-US-GuyNeural"

    DESCRIPTIONS_FILE_PATH: Path = BASE_DIR / "data" / "landmarks_descriptions.csv"

    class Config:
        env_file = ".env"

settings = Settings()