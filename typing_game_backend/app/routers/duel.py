from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from ...app import models,schemas
from ..database import get_db
from ..utils.elo import calculate_elo
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


@router.post("/result", response_model=schemas.MatchOut)
def record_match_result(
    player1_id: int,
    player2_id: int,
    winner_id: int,
    player1_wpm: float,
    player2_wpm: float,
    db: Session = Depends(get_db)
):
    # Fetch both players
    p1 = db.query(models.User).filter(models.User.id == player1_id).first()
    p2 = db.query(models.User).filter(models.User.id == player2_id).first()

    if not p1 or not p2:
        raise HTTPException(status_code=404, detail="Players not found")

    # Determine who won (1 or 2)
    winner = 1 if winner_id == p1.id else 2

    # Calculate new Elo scores
    new_elo1, new_elo2 = calculate_elo(p1.elo, p2.elo, winner)

    # Update player ratings
    p1.elo, p2.elo = new_elo1, new_elo2

    # Update seasonal points
    if winner == 1:
        p1.seasonal_points += 10
        p2.seasonal_points += 3
    else:
        p2.seasonal_points += 10
        p1.seasonal_points += 3

    # Create match record
    match = models.Match(
        player1_id=p1.id,
        player2_id=p2.id,
        winner_id=winner_id,
        player1_wpm=player1_wpm,
        player2_wpm=player2_wpm,
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return match