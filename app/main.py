from fastapi import FastAPI
from app.api.v1.routes import router
from app.db.database import lifespan

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def get_health():
  return {
    "status": "ok"
  }

app.include_router(router)
