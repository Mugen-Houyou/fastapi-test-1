from collections import defaultdict
from fastapi import WebSocket

class CallManager:
    """Manage WebRTC signaling connections per room."""

    def __init__(self) -> None:
        # room_id -> {username: WebSocket}
        self.active_connections: dict[str, dict[str, WebSocket]] = defaultdict(dict)

    async def connect(self, websocket: WebSocket, room_id: str, username: str) -> None:
        await websocket.accept()
        self.active_connections[room_id][username] = websocket

    async def disconnect(self, room_id: str, username: str) -> None:
        self.active_connections[room_id].pop(username, None)
        if not self.active_connections[room_id]:
            self.active_connections.pop(room_id, None)

    async def broadcast(self, room_id: str, message: dict, sender: str) -> None:
        for user, ws in self.active_connections[room_id].items():
            if user != sender:
                await ws.send_json(message)
