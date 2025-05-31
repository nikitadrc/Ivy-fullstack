from fastapi import WebSocket
from typing import Dict, Set
import json
import asyncio
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        # Store active connections
        self.active_connections: Dict[int, WebSocket] = {}
        # Store room memberships
        self.rooms: Dict[str, Set[int]] = {}
        # Message queue for each client
        self.message_queues: Dict[int, asyncio.Queue] = {}
        
    async def connect(self, websocket: WebSocket, client_id: int):
        """Connect a new client."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.message_queues[client_id] = asyncio.Queue()
        
    def disconnect(self, websocket: WebSocket, client_id: int):
        """Disconnect a client."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.message_queues:
            del self.message_queues[client_id]
        # Remove client from all rooms
        for room in self.rooms.values():
            room.discard(client_id)
            
    async def join_room(self, client_id: int, room_id: str):
        """Add a client to a room."""
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(client_id)
        
    async def leave_room(self, client_id: int, room_id: str):
        """Remove a client from a room."""
        if room_id in self.rooms:
            self.rooms[room_id].discard(client_id)
            if not self.rooms[room_id]:
                del self.rooms[room_id]
                
    async def broadcast(self, message: str):
        """Broadcast a message to all connected clients."""
        for connection in self.active_connections.values():
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                
    async def broadcast_to_room(self, room_id: str, message: str):
        """Broadcast a message to all clients in a specific room."""
        if room_id not in self.rooms:
            return
            
        for client_id in self.rooms[room_id]:
            if client_id in self.active_connections:
                try:
                    await self.active_connections[client_id].send_text(message)
                except Exception as e:
                    print(f"Error broadcasting to room {room_id}: {e}")
                    
    async def send_personal_message(self, client_id: int, message: str):
        """Send a message to a specific client."""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(message)
            except Exception as e:
                print(f"Error sending personal message to client {client_id}: {e}")
                
    async def broadcast_json(self, data: dict):
        """Broadcast a JSON message to all connected clients."""
        message = {
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        await self.broadcast(json.dumps(message))
        
    async def handle_interview_update(self, interview_id: str, update_type: str, data: dict):
        """Handle interview-related updates."""
        message = {
            "type": "interview_update",
            "interview_id": interview_id,
            "update_type": update_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_room(f"interview_{interview_id}", json.dumps(message))
        
    async def handle_analytics_update(self, user_id: int, data: dict):
        """Handle analytics-related updates."""
        message = {
            "type": "analytics_update",
            "user_id": user_id,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_personal_message(user_id, json.dumps(message))
        
    async def start_heartbeat(self):
        """Start sending heartbeat messages to all clients."""
        while True:
            await self.broadcast_json({"type": "heartbeat"})
            await asyncio.sleep(30)  # Send heartbeat every 30 seconds 