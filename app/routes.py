from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Register Route
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    # Registration logic here...
    pass

# ✅ ADD THIS
class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message
    bot_response = f"ZenifyAI says: You said '{user_message}'"
    return {"response": bot_response}
