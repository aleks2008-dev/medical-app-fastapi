from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set
import json

router = APIRouter()

# Storage of active WebSocket connections
connections: Set[WebSocket] = set()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            # We send a message to all connected users
            message = f"Broadcast: {data}"
            await broadcast_message(message)
    except WebSocketDisconnect:
        connections.discard(websocket)

@router.post("/broadcast")
async def send_broadcast(message: str):
    """Send a broadcast message to all connected clients"""
    sent_count = await broadcast_message(message)
    return {"message": "Broadcast sent", "sent_to": sent_count}

async def broadcast_message(message: str) -> int:
    """Send a message to all active connections"""
    if not connections:
        return 0
    
    disconnected = set()
    
    for connection in connections:
        try:
            await connection.send_text(message)
        except:
            disconnected.add(connection)
    
    # Removing disabled connections
    connections.difference_update(disconnected)
    
    return len(connections)

@router.get("/ws/status")
async def websocket_status():
    """Get the status of WebSocket connections"""
    return {
        "active_connections": len(connections),
        "status": "active" if connections else "no_connections"
    }