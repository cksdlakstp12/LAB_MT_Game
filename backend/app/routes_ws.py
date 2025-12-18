from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .models import HelperMessage, ExplorerActions
from .store import ROOM_STATES, ROOM_CONNECTIONS, init_room, broadcast_state
from .engine import apply_action, end_turn

router = APIRouter()


@router.websocket("/ws/{room_id}/{role}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, role: str):
    await websocket.accept()

    if room_id not in ROOM_CONNECTIONS:
        ROOM_CONNECTIONS[room_id] = {}
    ROOM_CONNECTIONS[room_id][role] = websocket

    # 방이 아직 없으면 기본 맵으로 생성
    if room_id not in ROOM_STATES:
        init_room(room_id, "sample")

    # 접속 직후 현재 상태 전송
    await broadcast_state(room_id)

    try:
        while True:
            data = await websocket.receive_json()
            state = ROOM_STATES[room_id]

            if state.is_over:
                await broadcast_state(room_id)
                continue

            msg_type = data.get("type")

            # 협력자 메시지
            if role == "helper" and msg_type == "helper_message":
                msg = HelperMessage(**data)
                if len(msg.message) == 2:
                    state.last_helper_message = msg.message
                await broadcast_state(room_id)

            # 탐색자 액션 (한 턴 최대 3회)
            elif role == "explorer" and msg_type == "explorer_actions":
                payload = ExplorerActions(**data)

                for act in payload.actions[:3]:
                    apply_action(state, act)

                # 한 번의 explorer_actions 요청을 1턴으로 처리
                end_turn(state)
                await broadcast_state(room_id)

    except WebSocketDisconnect:
        ROOM_CONNECTIONS.get(room_id, {}).pop(role, None)
    except Exception as e:
        print("Error in websocket:", e)
        ROOM_CONNECTIONS.get(room_id, {}).pop(role, None)
