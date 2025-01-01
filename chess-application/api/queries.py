from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from fastapi import APIRouter, Depends
from core.models.db_helper import db_helper

router = APIRouter()

@router.get("/search_players")
async def search_players(
    country: str,
    min_rating: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    query = text("""
        SELECT * FROM chess_players
        WHERE country = :country AND rating >= :min_rating
    """)
    result = await session.execute(query, {"country": country, "min_rating": min_rating})
    players = result.fetchall()
    return players