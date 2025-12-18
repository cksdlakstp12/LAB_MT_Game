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
    """
    backend/config.json 을 읽어서 Settings 생성.
    파일이 없거나 필드가 일부 비어 있어도 기본값으로 채워지도록 구성.
    """
    cfg_path = Path(__file__).resolve().parent.parent / "config.json"

    if not cfg_path.exists():
        # 설정 파일 없으면 기본값 사용
        return Settings()

    with cfg_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    return Settings(**raw)


# 애플리케이션 전체에서 사용할 전역 설정 객체
settings = load_settings()
