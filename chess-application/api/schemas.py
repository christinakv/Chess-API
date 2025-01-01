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