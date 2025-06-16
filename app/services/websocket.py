# app/services/websocket.py

# 이게 과연 app/services에 두는 게 적합한가?
# TODO: 실시간 서비스가 많아지면 나중에 app/realtime 같은 데다가 빼든지 해야 할 듯.

from fastapi import WebSocket
from collections import defaultdict

from ..core.redis_client import redis_client


class ConnectionManager:
    """Manage WebSocket connections per room."""

    def __init__(self) -> None:
        self.active_connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, room_id: str, username: str) -> None:
        await websocket.accept()
        self.active_connections[room_id].append(websocket)
        # 과거 메시지 전송
        history = await redis_client.lrange(f"room:{room_id}:messages", 0, -1)
        for message in history:
            await websocket.send_text(message)
        await self.send_message(room_id, f"{username} joined!")

    async def disconnect(self, websocket: WebSocket, room_id: str, username: str) -> None:
        self.active_connections[room_id].remove(websocket)
        await self.send_message(room_id, f"{username} left!")

    async def send_message(self, room_id: str, message: str) -> None:
        await redis_client.rpush(f"room:{room_id}:messages", message)
        for connection in self.active_connections[room_id]:
            await connection.send_text(message)
