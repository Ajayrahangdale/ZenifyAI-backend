from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ✅ User Registration Route (Fixed & Improved Error Handling)
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = utils.hash_password(user.password)
        new_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return schemas.UserResponse(id=new_user.id, name=new_user.name, email=new_user.email)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

#  User Login Route (Fixed & Debugging Added)
@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == form_data.username).first()
        
        if not user:
            print("[DEBUG] User not found")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not utils.verify_password(form_data.password, user.hashed_password):
            print("[DEBUG] Password verification failed")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = utils.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

#  Get User Route (Fixed & Improved)
@router.get("/user/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return schemas.UserResponse(id=user.id, name=user.name, email=user.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


