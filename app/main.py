from fastapi import FastAPI
from app.db.database import lifespan

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def get_health():
  return {
    "status": "ok"
  }
