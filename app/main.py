from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import routes, models
from app.database import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# ✅ Define correct origins
origins = [
    "http://localhost:5173",       # Vite dev server
    "https://zenifyai.vercel.app", # Production frontend
]

# ✅ Use origins variable properly here
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Fix this line
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "ZenifyAI Backend is Live!"}
