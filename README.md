# basicPythonFastApi

FastAPI project with JWT auth, MongoDB integration, and Docker support.

## Run locally

```bash
fastapi dev app/main.py
```

## Run with Docker

```bash
docker compose up --build
```

The API will be available at `http://127.0.0.1:8000` and the docs at `http://127.0.0.1:8000/docs`.

## Environment variables

Create a `.env` file with values like:

```dotenv
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
TIMEZONE=America/El_Salvador
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=local
```
