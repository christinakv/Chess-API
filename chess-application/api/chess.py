from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models.db_helper import db_helper
from core.models.chess_player import ChessPlayer
from .schemas import ChessPlayerCreate, ChessPlayerResponse

router = APIRouter()

@router.get("/chess_players", response_model=list[ChessPlayerResponse])
async def get_chess_players(session: AsyncSession = Depends(db_helper.session_getter)):
    result = await session.execute(select(ChessPlayer))
    players = result.scalars().all()
    return players

@router.post("/chess_players", response_model=ChessPlayerResponse)
async def add_chess_player(player: ChessPlayerCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    new_player = ChessPlayer(**player.dict())
    session.add(new_player)
    await session.commit()
    await session.refresh(new_player)  # Refresh to get the updated data
    return new_player