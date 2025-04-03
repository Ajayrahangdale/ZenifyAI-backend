from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import routes, models  
from app.database import engine

# ✅ सबसे पहले FastAPI app define करो
app = FastAPI()

# ✅ अब middleware add करो
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # सभी origins को allow कर रहा है
    allow_credentials=True,
    allow_methods=["*"],  # सभी HTTP methods को allow कर रहा है
    allow_headers=["*"],  # सभी headers को allow कर रहा है
)

# ✅ Database Tables Create करो
print(f"Database Engine: {engine}")
models.Base.metadata.create_all(bind=engine)

# ✅ Routes include करो
app.include_router(routes.router)


