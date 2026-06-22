from fastapi import FastAPI

from src.handlers.general import router as general_router

app = FastAPI()

app.include_router(general_router, prefix="/api/v1")


@app.get("/ping")
def healthcheck():
    return {"status": "pong"}
