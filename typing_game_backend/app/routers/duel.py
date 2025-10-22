from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

router = APIRouter(prefix="/duel", tags=["Duel"])

# keep active rooms in memory (later we’ll store in Redis)
active_rooms: Dict[str, List[WebSocket]] = {}

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()

    if room_id not in active_rooms:
        active_rooms[room_id] = []
    active_rooms[room_id].append(websocket)

    try:
        while True:
            # inside the receive loop
            data = json.loads(await websocket.receive_text())

            #for example {"type": "progress", "progress": 57}
            if data["type"] == "progress":
                for client in active_rooms[room_id]:
                    if client != websocket:
                        await client.send_text(json.dumps(data))
            elif data["type"] == "finished":
                #brodcast that this player has finished typing
                for client in active_rooms[room_id]:
                    await client.send_text(json.dumps({"type": "result", "message": f"{data['player']} finished "}))
                
    except WebSocketDisconnect:
        active_rooms[room_id].remove(websocket)
        if not active_rooms[room_id]:
            del active_rooms[room_id]