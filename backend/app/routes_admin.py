# backend/app/routes_admin.py
from typing import List
from fastapi import APIRouter, HTTPException

from .models import MapModel, GameState, CreateRoomRequest
from .store import MAPS, ROOM_STATES, init_room, upsert_map, delete_map, load_maps_from_disk

router = APIRouter()


@router.get("/maps", response_model=List[MapModel])
def list_maps():
    return list(MAPS.values())


@router.get("/maps/{map_id}", response_model=MapModel)
def get_map(map_id: str):
    if map_id not in MAPS:
        raise HTTPException(status_code=404, detail="Unknown map_id")
    return MAPS[map_id]


@router.post("/maps", response_model=MapModel)
def create_or_update_map(map_model: MapModel):
    return upsert_map(map_model)


@router.delete("/maps/{map_id}")
def remove_map(map_id: str):
    if map_id not in MAPS:
        raise HTTPException(status_code=404, detail="Unknown map_id")
    delete_map(map_id)
    return {"ok": True}


@router.post("/maps/reload", response_model=List[MapModel])
def reload_maps():
    load_maps_from_disk()
    return list(MAPS.values())


@router.post("/rooms", response_model=GameState)
def create_room(req: CreateRoomRequest):
    return init_room(req.room_id, req.map_id)


@router.get("/rooms/{room_id}", response_model=GameState)
def get_room(room_id: str):
    if room_id not in ROOM_STATES:
        raise HTTPException(status_code=404, detail="Unknown room_id")
    return ROOM_STATES[room_id]
