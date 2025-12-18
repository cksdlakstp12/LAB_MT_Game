from typing import List
from fastapi import APIRouter, HTTPException
from .models import MapModel, GameState, CreateRoomRequest
from .store import MAPS, ROOM_STATES, init_room

router = APIRouter()


@router.get("/maps", response_model=List[MapModel])
def list_maps():
    return list(MAPS.values())


@router.post("/rooms", response_model=GameState)
def create_room(req: CreateRoomRequest):
    return init_room(req.room_id, req.map_id)


@router.get("/rooms/{room_id}", response_model=GameState)
def get_room(room_id: str):
    if room_id not in ROOM_STATES:
        raise HTTPException(status_code=404, detail="Unknown room_id")
    return ROOM_STATES[room_id]
