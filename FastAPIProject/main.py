from fastapi import FastAPI

from src.handlers.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1")


@app.get("/ping")
def healthcheck():
    return {"status": "pong"}
