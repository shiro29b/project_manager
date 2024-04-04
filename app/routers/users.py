
from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..database import engine,get_db
from .. import models,schemas,utils
from fastapi import Depends,status , HTTPException, APIRouter


router =  APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate,db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    valid_roles = ["SuperAdmin", "Admin", "Client"]
    if user.role not in valid_roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role. Allowed roles are 'SuperAdmin', 'Admin', and 'Client'")

    if existing_user:
        # If user already exists, raise an HTTPException with status code 400 (Bad Request)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    user.password= utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user