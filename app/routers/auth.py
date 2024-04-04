
from fastapi import Depends ,status , HTTPException , APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils,oauth2

from fastapi.security import OAuth2PasswordRequestForm

router= APIRouter(
    tags=["Authentication"]
)

@router.post("/login",response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm=Depends(),db : Session = Depends(get_db)):
    
    user = db.query(models.User).filter(user_credentials.username ==models.User.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")

    access_token= oauth2.create_acces_token(data={"user_id":user.id})
    
    return {"access_token": access_token,"token_type":"bearer"}