# backend/app/config.py
from pathlib import Path
from typing import List
from pydantic import BaseModel
import json


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class CorsConfig(BaseModel):
    allow_origins: List[str] = ["*"]


class Settings(BaseModel):
    server: ServerConfig = ServerConfig()
    cors: CorsConfig = CorsConfig()


def load_settings() -> Settings:
    cfg_path = Path(__file__).resolve().parent.parent / "config.json"

    if not cfg_path.exists():
        return Settings()

    with cfg_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    return Settings(**raw)


settings = load_settings()
