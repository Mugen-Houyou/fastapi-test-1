from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

from app.services.webrtc import CallManager

router = APIRouter()
manager = CallManager()


@router.websocket("/ws/webrtc/{room_id}")
async def webrtc_endpoint(websocket: WebSocket, room_id: str, username: str):
    """WebRTC signaling endpoint."""
    await manager.connect(websocket, room_id, username)
    try:
        while True:
            text = await websocket.receive_text()
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                data = {"type": "message", "payload": text}
            await manager.broadcast(room_id, data, sender=username)
    except WebSocketDisconnect:
        await manager.disconnect(room_id, username)
