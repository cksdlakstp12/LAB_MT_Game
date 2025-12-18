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

    # 맵 밖이면 이동 무시
    if nx < 0 or ny < 0 or nx >= game_map.width or ny >= game_map.height:
        return

    tile = game_map.cells[ny][nx]

    # 바위는 이동 불가
    if tile == "rock":
        return

    # 이동
    state.explorer_x = nx
    state.explorer_y = ny

    # 함정 처리 (TODO: 상세 규칙 반영)
    if tile == "trap":
        # 예시: 생명 감소 후 턴 종료 로직은 routes_ws에서 추가
        pass

    # 보물
    if tile == "treasure":
        state.treasures_found += 1
        game_map.cells[ny][nx] = "empty"

    # 몬스터 처리 (TODO: 몬스터 이동 및 충돌)
    # if tile == "monster": ...


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

    # 종료 조건
    if state.turn > state.max_turn:
        state.is_over = True
        state.winner = "timeout"

    if state.treasures_found >= state.total_treasures and state.total_treasures > 0:
        state.is_over = True
        state.winner = "explorer"

    # TODO: explorer_lives가 0이 되었을 때 승패 처리, 여러 팀 비교 등
