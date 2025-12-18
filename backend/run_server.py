import uvicorn
from app.main import app  # 이미 create_app() 호출된 app 객체
from app.config import settings


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=True,
    )
