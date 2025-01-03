# Chess API

A **FastAPI** application that uses **SQLAlchemy** and **PostgreSQL** to manage chess players, tournaments, and participants. The project is managed with **Poetry**, and automatically seeds the database from JSON files when it’s empty.

---

## Features

- **Database Creation & Seeding**  
  - On startup, the app creates tables if they don’t exist.  
  - If the database is empty, it loads sample data from JSON files into the DB.
- **API Endpoints** for:
  - Listing/Filtering/Sorting chess players
  - Retrieving a single player
  - Showing tournaments a player participates in
  - Updating a player’s rating
- **Automatic Documentation**  
  - Interactive Swagger UI at `/docs`  
  - Redoc UI at `/redoc`  

---

## Table of Contents

1. [Requirements](#requirements)  
2. [Installation](#installation)  
3. [Usage](#usage)  
4. [API Endpoints](#api-endpoints)  
5. [Project Structure](#project-structure)  

---

## Requirements

- **Python 3.9+**  
- **Poetry** for dependency management  
- **PostgreSQL** (local or Docker-based)  

*(If you use Docker Compose, you might have a `docker-compose.yml` that spins up Postgres.)*

---

## Installation

1. **Clone** the repository:

`git clone https://github.com/your-username/Chess-API.git`

`cd Chess-API`

2. **Install dependencies** using Poetry:

`poetry install`

This will create a virtual environment (if not already existing) and install the packages specified in **`pyproject.toml`**.

3. **Activate the Poetry shell** (optional, but recommended):

`poetry shell`

This drops you into an environment with all dependencies available.

4. **Configure Database**  
- Update `core/config.py` or `.env` (if you use environment variables) to match your **PostgreSQL** connection string, e.g. `postgresql+asyncpg://root:password@localhost:5432/postgres`.  
- If using Docker, run `docker-compose up -d` to spin up your Postgres container on port 5432.

---

## Usage

### Start the Application

From the root directory (where `pyproject.toml` is located), run:

poetry run uvicorn chess-application.main:main_app –host 127.0.0.1 –port 8000 –reload
- **`chess-application.main:main_app`** is the import string:
  - `chess-application/main.py` is the module
  - `main_app` is the FastAPI instance inside that file
- `--reload` enables auto-reloading on code changes.

If you **activated** the Poetry shell via `poetry shell`, you can also do:

`uvicorn chess-application.main:main_app –host 127.0.0.1 –port 8000 –reload`
*(No `poetry run` prefix needed since you’re in the environment.)*

### Verify It’s Working

- Visit **http://127.0.0.1:8000** to see a basic welcome page (`index.html`).  
- Visit **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

### Automatic Database Seeding

On startup, the app:

1. Creates tables (if missing).  
2. Checks if the DB is empty (no `ChessPlayer` records).  
3. If empty, reads JSON files (`chess_players.json`, `tournaments.json`, `participants.json`) and inserts them into the DB.

---

## API Endpoints

Below is a summary (see `/docs` for complete details):

1. **Get All Chess Players**  
   - `GET /chess_players`  
   - Returns all chess players.

2. **Get Player by ID**  
   - `GET /chess_players/id/{player_id}`  
   - Returns a specific player.

3. **Filter Players**  
   - `GET /chess_players/filtered?country=USA&rating_min=2700`  
   - Filters by country & rating minimum.

4. **Average Rating by Country**  
   - `GET /chess_players/average_rating_by_country`

5. **Sorted Players**  
   - `GET /chess_players/sorted?sort_by=rating&sort_order=asc|desc`

6. **With Tournament**  
   - `GET /chess_players/with_tournament/{player_id}`  
   - Returns a player plus any tournaments they’re participating in.

7. **Update Player Rating**  
   - `PUT /chess_players/update_rating/{player_id}?new_rating=2850`  
   - Updates the player’s rating if `new_rating` > current rating.

---

## Project Structure

A simplified layout:
<h2>Project Structure</h2>

<pre>
Chess-API/
├─ pyproject.toml             # Poetry config (package metadata & dependencies)
├─ poetry.lock                # Generated lockfile
├─ docker-compose.yml         # (Optional) For local Postgres
├─ chess-application/
│  ├─ main.py                 # Main FastAPI application
│  └─ core/
│     ├─ config.py            # Database URL & settings
│     └─ models/
│        ├─ base.py           # SQLAlchemy Base
│        ├─ db_helper.py      # AsyncSession engine creation
│        ├─ chess_player.py   # ChessPlayer model
│        ├─ tournament.py     # Tournament model
│        ├─ participant.py    # Participant model
│        ├─ chess_players.json
│        ├─ tournaments.json
│        └─ participants.json
├─ ui/
│  └─ index.html
└─ README.md
</pre>