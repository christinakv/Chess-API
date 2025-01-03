import json
from typing import List

from core.models import ChessPlayer
from core.db_helper import get_session


def load_data_from_json(filename: str) -> List[dict]:
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found - {filename}")
        raise
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file - {filename}")
        raise


def populate_database(data: List[dict], session):
    for player_data in data:
        player = ChessPlayer(**player_data)
        try:
            session.add(player)
            session.commit()
            print(f"Player added successfully: {player.name}")
        except Exception as e:
            print(f"Error adding player: {player.name}")
            print(f"Error details: {e}")
            session.rollback()


if __name__ == "__main__":
    player_data_file = "players.json"

    try:
        data = load_data_from_json(player_data_file)

        session = get_session()

        populate_database(data, session)

        print("Database population completed!")

    finally:
        if session:
            session.close()