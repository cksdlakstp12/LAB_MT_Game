from typing import List, Optional, Literal
from pydantic import BaseModel

TileType = Literal["empty", "rock", "trap", "treasure", "monster", "start"]


class MapModel(BaseModel):
    id: str
    name: str
    width: int
    height: int
    cells: List[List[TileType]]


class GameState(BaseModel):
    room_id: str
    map_id: str
    turn: int = 1
    max_turn: int = 50

    explorer_lives: int = 3
    explorer_x: int
    explorer_y: int
    explorer_dir: int  # 0: up, 1: right, 2: down, 3: left

    treasures_found: int = 0
    total_treasures: int = 0

    is_over: bool = False
    winner: Optional[str] = None

    last_helper_message: Optional[str] = None


class CreateRoomRequest(BaseModel):
    room_id: str
    map_id: str


class HelperMessage(BaseModel):
    type: Literal["helper_message"]
    message: str


class ExplorerActions(BaseModel):
    type: Literal["explorer_actions"]
    actions: List[Literal["F", "L", "R"]]
