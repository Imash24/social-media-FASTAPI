from .. import models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Response , status, APIRouter
from .. database import  engine, get_db


router = APIRouter(prefix="/users"
                   ,tags=["users"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def CreateUser(user: schemas.UserCreate,db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
    
    
    
@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == id).first()
    
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The user with id:{id} is not found")
    
    return users
        
        


        
        
        
