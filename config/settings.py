import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API 配置
    OPENAI_API_KEY: str = Field(default=..., env="OPENAI_API_KEY")
    OPENAI_MODEL_NAME: str = "gpt-4-1106-preview" # 或 gpt-4o
    
    # 游戏配置
    LOG_LEVEL: str = "INFO"
    GAME_TIMEOUT_SECONDS: int = 600
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# 单例实例
settings = Settings()