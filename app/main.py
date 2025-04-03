import os
from fastapi import FastAPI
from app import routes, models  # ✅ Correct Import Path
from app.database import engine  # ✅ Correct Import Path

# Ensure that models.Base is correctly imported
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include router from routes
app.include_router(routes.router)
