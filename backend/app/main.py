from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import uvicorn

from .routes import router as conversation_router
from .discovery_routes import router as discovery_router
from .database import engine
from . import models  # Import models to ensure they are registered

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dating App API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config('FRONTEND_URL', default="http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization"],
    expose_headers=["*"],
)

# Include our routes
app.include_router(conversation_router, prefix="/api")
app.include_router(discovery_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)