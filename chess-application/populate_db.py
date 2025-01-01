import requests

BASE_URL = "http://localhost:8000/api"

def populate_chess_players():
    for i in range(1, 101):
        payload = {
            "chess_player_id": i,
            "first_name": f"Player{i}",
            "last_name": f"Last{i}",
            "country": "Country",
            "world_rank": i,
            "rating": 2500 + i,
            "title": "GM" if i % 2 == 0 else "IM"
        }
        requests.post(f"{BASE_URL}/chess/chess_players", json=payload)

def populate_tournaments():
    for i in range(1, 21):
        payload = {
            "tournament_id": i,
            "tournament_name": f"Tournament{i}",
            "country": "Country",
            "city": "City",
            "date": "2025-01-01",
            "qualification": "Open"
        }
        requests.post(f"{BASE_URL}/chess/tournaments", json=payload)

if __name__ == "__main__":
    populate_chess_players()
    populate_tournaments()