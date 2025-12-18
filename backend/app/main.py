# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes_admin import router as admin_router
from .routes_ws import router as ws_router
from .store import MAPS, load_maps_from_disk, init_room, ROOM_STATES
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

    app.include_router(admin_router)
    app.include_router(ws_router)

    @app.on_event("startup")
    async def startup_event():
        load_maps_from_disk()
        if "demo" not in ROOM_STATES:
            init_room("demo", "sample")

    return app


app = create_app()
