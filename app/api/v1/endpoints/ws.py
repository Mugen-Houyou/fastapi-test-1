from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.websocket import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/chat/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str):
    """WebSocket endpoint for chat rooms."""
    await manager.connect(websocket, room_id, username)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(room_id, f"{username}: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket, room_id, username)
