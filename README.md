# Backend Assignment - Task 1

## API Key & Rate Limiting Service (FastAPI)

This project implements Task 1 from the assignment:

- API credential generation
- Secure credential storage (hashed API keys)
- Per-credential usage tracking
- Rate limiting (`5 requests / 60 seconds` per credential)
- Protected APIs requiring valid API key
- Swagger docs at `/docs`

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pytest

## Project Structure

```text
app/
  main.py
  database.py
  models.py
  schemas.py
  dependencies.py
  routers/
    credentials.py
    protected.py
  services/
    security.py
tests/
  test_task1_service.py
postman_task1_collection.json
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

App URL: `http://127.0.0.1:8000`  
Docs URL: `http://127.0.0.1:8000/docs`

## Endpoints

1. `POST /api-key`
Generate a unique API key.

2. `GET /data`
Protected endpoint, requires header `x-api-key`.

3. `GET /usage`
Returns usage summary for the same API key.

## Rate Limiting Rules

- Window: 60 seconds
- Limit: 5 requests per API key inside one window
- Exceeded requests return HTTP `429`

## Testing

```bash
pytest -q
```

## Postman

Import file:

- `postman_task1_collection.json`
