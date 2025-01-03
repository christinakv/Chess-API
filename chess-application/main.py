from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from typing import Optional
import os
import json
from core.utils import json_to_dict_list

# JSON file paths
path_to_json_chess_players = os.path.join(os.path.dirname(__file__), 'core', 'models', 'chess_players.json')
path_to_json_tournaments   = os.path.join(os.path.dirname(__file__), 'core', 'models', 'tournaments.json')
path_to_json_participants  = os.path.join(os.path.dirname(__file__), 'core', 'models', 'participants.json')

main_app = FastAPI()

@main_app.get("/")
def root():
    return FileResponse("../ui/index.html")

@main_app.get("/chess_players")
async def get_all_chess_players():
    players = json_to_dict_list(path_to_json_chess_players)
    if not players:
        raise HTTPException(status_code=404, detail="No chess players found.")
    return players

@main_app.get("/chess_players/id/{player_id}")
async def get_chess_player_by_id(player_id: int):
    players = json_to_dict_list(path_to_json_chess_players)
    # Find the player with matching ID
    player = next((p for p in players if p["chess_player_id"] == player_id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@main_app.get("/chess_players/filtered")
async def get_filtered_players(
    country: Optional[str] = None,
    rating_min: Optional[int] = None
):
    players = json_to_dict_list(path_to_json_chess_players)
    filtered = []
    for p in players:
        if (country is None or p["country"] == country) and \
           (rating_min is None or p["rating"] >= rating_min):
            filtered.append(p)

    if not filtered:
        raise HTTPException(status_code=404, detail="No players found with the given filters.")
    return filtered

@main_app.get("/chess_players/average_rating_by_country")
async def get_average_rating_by_country():
    players = json_to_dict_list(path_to_json_chess_players)
    if not players:
        raise HTTPException(status_code=404, detail="No data available.")

    from collections import defaultdict
    country_to_ratings = defaultdict(list)

    for p in players:
        country_to_ratings[p["country"]].append(p["rating"])

    result = []
    for country, ratings in country_to_ratings.items():
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        result.append({"country": country, "average_rating": avg_rating})

    return result

@main_app.get("/chess_players/sorted")
async def get_sorted_players(
    sort_by: str = Query("rating", enum=["rating", "world_rank"]),
    sort_order: str = Query("desc", enum=["asc", "desc"])
):
    players = json_to_dict_list(path_to_json_chess_players)

    reverse_sort = (sort_order == "desc")
    sorted_players = sorted(players, key=lambda p: p[sort_by], reverse=reverse_sort)

    if not sorted_players:
        raise HTTPException(status_code=404, detail="No players found.")
    return sorted_players

@main_app.get("/chess_players/with_tournament/{player_id}")
async def get_player_with_tournament(player_id: int):
    players = json_to_dict_list(path_to_json_chess_players)
    tournaments = json_to_dict_list(path_to_json_tournaments)
    participants = json_to_dict_list(path_to_json_participants)

    player = next((p for p in players if p["chess_player_id"] == player_id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player_tournament_ids = [
        part["tournament_id"] for part in participants
        if part["chess_player_id"] == player_id
    ]
    player_tournaments = [
        t for t in tournaments
        if t["tournament_id"] in player_tournament_ids
    ]

    return {
        "player": player,
        "tournaments": player_tournaments
    }

@main_app.put("/chess_players/update_rating/{player_id}")
async def update_player_rating(player_id: int, new_rating: int):
    players = json_to_dict_list(path_to_json_chess_players)

    player_index = None
    for i, p in enumerate(players):
        if p["chess_player_id"] == player_id:
            player_index = i
            break

    if player_index is None:
        raise HTTPException(status_code=404, detail="Player not found")

    current_rating = players[player_index]["rating"]
    if new_rating <= current_rating:
        raise HTTPException(status_code=400, detail="New rating must be higher than the current rating.")

    players[player_index]["rating"] = new_rating

    with open(path_to_json_chess_players, 'w', encoding='utf-8') as f:
        json.dump(players, f, indent=4)

    return {
        "message": "Player's rating updated",
        "player": players[player_index]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="127.0.0.1", port=8000, reload=False)