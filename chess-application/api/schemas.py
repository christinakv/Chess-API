from pydantic import BaseModel
from typing import Optional

class ChessPlayerCreate(BaseModel):
    chess_player_id: int
    first_name: str
    last_name: str
    country: str
    world_rank: int
    rating: int
    title: str

class ChessPlayerResponse(ChessPlayerCreate):
    id: int

    class Config:
        orm_mode = True

class ParticipantCreate(BaseModel):
    participant_id: int
    tournament_id: int
    chess_player_id: int
    place: int

class TournamentCreate(BaseModel):
    tournament_id: int
    tournament_name: str
    country: str
    city: str
    date: str
    qualification: str
