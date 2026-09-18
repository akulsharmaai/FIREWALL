import logging
from typing import List, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    environment: str = "development"
    debug: bool = True
    
    # Model Settings
    model_mode: Literal["mock", "real"] = "mock"
    model_path: str = "./models/model.pkl"
    
    # CORS Settings
    cors_origins: str = "*"
    
    # Logging
    log_level: str = "INFO"

    @property
    def cors_origin_list(self) -> List[str]:
        if not self.cors_origins:
            return []
        return [origin.strip() for origin in self.cors_origins.split(",")]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

# Instantiate settings
settings = Settings()
