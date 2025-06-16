from fastapi import WebSocket
from collections import defaultdict


class ConnectionManager:
    """Manage WebSocket connections per room."""

    def __init__(self) -> None:
        self.active_connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, room_id: str, username: str) -> None:
        await websocket.accept()
        self.active_connections[room_id].append(websocket)
        await self.send_message(room_id, f"{username} joined!")

    async def disconnect(self, websocket: WebSocket, room_id: str, username: str) -> None:
        self.active_connections[room_id].remove(websocket)
        await self.send_message(room_id, f"{username} left!")

    async def send_message(self, room_id: str, message: str) -> None:
        for connection in self.active_connections[room_id]:
            await connection.send_text(message)
