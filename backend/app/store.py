from typing import Dict
from fastapi import WebSocket, HTTPException
from .models import MapModel, GameState, TileType

# 인메모리 저장소 (개발용)
MAPS: Dict[str, MapModel] = {}
ROOM_STATES: Dict[str, GameState] = {}
ROOM_CONNECTIONS: Dict[str, Dict[str, WebSocket]] = {}  # room_id -> {role: ws}


def create_sample_map() -> MapModel:
    # 7x7 샘플 맵
    width, height = 7, 7
    cells: list[list[TileType]] = [["empty" for _ in range(width)] for _ in range(height)]

    # 시작 위치
    cells[3][3] = "start"

    # 보물
    cells[1][5] = "treasure"
    cells[5][1] = "treasure"

    # 바위, 함정, 몬스터
    cells[2][2] = "rock"
    cells[4][4] = "trap"
    cells[2][4] = "monster"

    return MapModel(
        id="sample",
        name="Sample Map",
        width=width,
        height=height,
        cells=cells,
    )


def init_room(room_id: str, map_id: str) -> GameState:
    if map_id not in MAPS:
        raise HTTPException(status_code=404, detail="Unknown map_id")

    game_map = MAPS[map_id]

    start_x, start_y = 0, 0
    total_treasures = 0

    for y in range(game_map.height):
        for x in range(game_map.width):
            tile = game_map.cells[y][x]
            if tile == "start":
                start_x, start_y = x, y
            if tile == "treasure":
                total_treasures += 1

    state = GameState(
        room_id=room_id,
        map_id=map_id,
        explorer_x=start_x,
        explorer_y=start_y,
        explorer_dir=0,
        total_treasures=total_treasures,
    )
    ROOM_STATES[room_id] = state
    return state


async def broadcast_state(room_id: str):
    state = ROOM_STATES[room_id]
    payload = {
        "type": "state",
        "state": state.dict(),
    }
    conns = ROOM_CONNECTIONS.get(room_id, {})
    for role, ws in list(conns.items()):
        try:
            await ws.send_json(payload)
        except Exception:
            # 끊긴 소켓은 일단 무시
            pass
