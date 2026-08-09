from fastapi import FastAPI,APIRouter

from routes.ask import router as ask_router
from routes.upload import router as upload_router

app = FastAPI()

app.include_router(ask_router)
app.include_router(upload_router)

@app.get("/")
def home():

    return {
        "message" : "API connected successfully"
    }

@app.get("/health")
def get_health():

    return {
        "status" : "healthy"
    }

