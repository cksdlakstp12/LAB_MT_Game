# backend/app/engine.py
from .models import GameState
from .store import MAPS


def step_forward(state: GameState):
    game_map = MAPS[state.map_id]

    dir_to_vec = {
        0: (0, -1),   # up
        1: (1, 0),    # right
        2: (0, 1),    # down
        3: (-1, 0),   # left
    }

    dx, dy = dir_to_vec[state.explorer_dir]
    nx = state.explorer_x + dx
    ny = state.explorer_y + dy

    if nx < 0 or ny < 0 or nx >= game_map.width or ny >= game_map.height:
        return

    tile = game_map.cells[ny][nx]

    if tile == "rock":
        return

    state.explorer_x = nx
    state.explorer_y = ny

    if tile == "trap":
        # TODO: 함정 효과 추가 (생명 감소, 턴 종료 등)
        pass

    if tile == "treasure":
        state.treasures_found += 1
        game_map.cells[ny][nx] = "empty"

    # TODO: monster 처리


def apply_action(state: GameState, action: str):
    if action == "F":
        step_forward(state)
    elif action == "L":
        state.explorer_dir = (state.explorer_dir - 1) % 4
    elif action == "R":
        state.explorer_dir = (state.explorer_dir + 1) % 4


def end_turn(state: GameState):
    state.turn += 1
    state.last_helper_message = None

    if state.turn > state.max_turn:
        state.is_over = True
        state.winner = "timeout"

    if state.treasures_found >= state.total_treasures and state.total_treasures > 0:
        state.is_over = True
        state.winner = "explorer"

    # TODO: explorer_lives 0 시 처리 등
