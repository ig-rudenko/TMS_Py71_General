from fastapi import FastAPI

from src.handlers.auth import router as auth_router
from src.handlers.ws import router as ws_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1")
app.include_router(ws_router)


@app.get("/ping")
def healthcheck():
    return {"status": "pong"}
