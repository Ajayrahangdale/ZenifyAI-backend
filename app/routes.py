from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import models, schemas, utils
from .database import get_db

# 👇 New Imports for AI
from openai import OpenAI  # ✅ Corrected import
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ OpenAI client setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

# ✅ Chat Schema
class ChatRequest(BaseModel):
    message: str

# ✅ Chat Route using OpenAI
@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        user_message = request.message
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ZenifyAI, a helpful and kind mental health assistant. You give empathetic and supportive advice."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message.content
        return {"response": bot_reply}
    except Exception as e:
        print("🔥 AI Error:", e)
        return {"response": f"❌ AI Error: {str(e)}"}

# ✅ User Registration
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = utils.hash_password(user.password)
    new_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return schemas.UserResponse(id=new_user.id, name=new_user.name, email=new_user.email)
