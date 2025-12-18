from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes_admin import router as admin_router
from .routes_ws import router as ws_router
from .store import MAPS, create_sample_map, init_room
from .config import settings


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app.include_router(admin_router)
    app.include_router(ws_router)

    @app.on_event("startup")
    async def startup_event():
        # 샘플 맵, 데모 룸 생성
        if "sample" not in MAPS:
            MAPS["sample"] = create_sample_map()
        # demo 방 초기화
        if "demo" not in MAPS:
            # 위에서 이미 sample 맵을 넣었으므로 별도 작업 없음
            pass
        init_room("demo", "sample")

    return app


app = create_app()
