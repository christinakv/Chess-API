from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from typing import Optional
import json
import os

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import engine, AsyncSessionLocal, get_db_session
from core.models.base import Base
from core.models.chess_player import ChessPlayer
from core.models.tournament import Tournament
from core.models.participant import Participant

BASE_DIR = os.path.dirname(__file__)
PATH_PLAYERS = os.path.join(BASE_DIR, "core", "models", "chess_players.json")
PATH_TOURNAMENTS = os.path.join(BASE_DIR, "core", "models", "tournaments.json")
PATH_PARTICIPANTS = os.path.join(BASE_DIR, "core", "models", "participants.json")

main_app = FastAPI()

@main_app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = AsyncSessionLocal()
    try:
        result = await async_session.execute(select(func.count(ChessPlayer.chess_player_id)))
        count = result.scalar()
        if count == 0:
            await populate_db(async_session)
    finally:
        await async_session.close()

async def populate_db(db: AsyncSession):
    def load_json(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    players_data = load_json(PATH_PLAYERS)
    tournaments_data = load_json(PATH_TOURNAMENTS)
    participants_data = load_json(PATH_PARTICIPANTS)

    for p in players_data:
        db.add(ChessPlayer(**p))

    for t in tournaments_data:
        db.add(Tournament(**t))

    await db.flush()

    for part in participants_data:
        db.add(Participant(**part))

    await db.commit()
    print("Database populated from JSON files!")

@main_app.get("/")
def root():
    return FileResponse("../ui/index.html")

@main_app.get("/chess_players")
async def get_all_chess_players(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(ChessPlayer))
    players = result.scalars().all()
    if not players:
        raise HTTPException(status_code=404, detail="No chess players found.")
    return players

@main_app.get("/chess_players/id/{player_id}")
async def get_chess_player_by_id(player_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(ChessPlayer).where(ChessPlayer.chess_player_id == player_id))
    player = result.scalars().first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@main_app.get("/chess_players/filtered")
async def get_filtered_players(
    db: AsyncSession = Depends(get_db_session),
    country: Optional[str] = None,
    rating_min: Optional[int] = None
):
    stmt = select(ChessPlayer)
    if country:
        stmt = stmt.where(ChessPlayer.country == country)
    if rating_min:
        stmt = stmt.where(ChessPlayer.rating >= rating_min)

    result = await db.execute(stmt)
    filtered = result.scalars().all()
    if not filtered:
        raise HTTPException(status_code=404, detail="No players found with the given filters.")
    return filtered

@main_app.get("/chess_players/average_rating_by_country")
async def get_average_rating_by_country(db: AsyncSession = Depends(get_db_session)):
    stmt = (
        select(
            ChessPlayer.country,
            func.avg(ChessPlayer.rating).label("average_rating")
        )
        .group_by(ChessPlayer.country)
    )
    result = await db.execute(stmt)
    data = result.all()
    if not data:
        raise HTTPException(status_code=404, detail="No data available.")
    return [{"country": row[0], "average_rating": row[1]} for row in data]

@main_app.get("/chess_players/sorted")
async def get_sorted_players(
    sort_by: str = Query("rating", enum=["rating", "world_rank"]),
    sort_order: str = Query("desc", enum=["asc", "desc"]),
    db: AsyncSession = Depends(get_db_session)
):
    column = getattr(ChessPlayer, sort_by)
    if sort_order == "desc":
        column = column.desc()
    stmt = select(ChessPlayer).order_by(column)

    result = await db.execute(stmt)
    players = result.scalars().all()
    if not players:
        raise HTTPException(status_code=404, detail="No players found.")
    return players

@main_app.get("/chess_players/with_tournament/{player_id}")
async def get_player_with_tournament(player_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(ChessPlayer).where(ChessPlayer.chess_player_id == player_id))
    player = result.scalars().first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    part_stmt = select(Participant.tournament_id).where(Participant.chess_player_id == player_id)
    part_result = await db.execute(part_stmt)
    tournament_ids = [row[0] for row in part_result]

    if not tournament_ids:
        return {"player": player, "tournaments": []}

    tour_stmt = select(Tournament).where(Tournament.tournament_id.in_(tournament_ids))
    tour_result = await db.execute(tour_stmt)
    tournaments = tour_result.scalars().all()

    return {
        "player": player,
        "tournaments": tournaments
    }

@main_app.put("/chess_players/update_rating/{player_id}")
async def update_player_rating(
    player_id: int,
    new_rating: int,
    db: AsyncSession = Depends(get_db_session)
):
    result = await db.execute(select(ChessPlayer).where(ChessPlayer.chess_player_id == player_id))
    player = result.scalars().first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    if new_rating <= player.rating:
        raise HTTPException(status_code=400, detail="New rating must be higher than current rating.")

    player.rating = new_rating
    await db.commit()
    await db.refresh(player)

    return {
        "message": "Player's rating updated",
        "player": player
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:main_app", host="127.0.0.1", port=8000, reload=True)