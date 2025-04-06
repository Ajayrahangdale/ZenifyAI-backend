import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ CORS import
from app import routes, models  # ✅ Correct Import Path
from app.database import engine  # ✅ Correct Import Path

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routes
app.include_router(routes.router)

# Basic test route
@app.get("/")
def read_root():
    return {"message": "ZenifyAI Backend is Live!"}
