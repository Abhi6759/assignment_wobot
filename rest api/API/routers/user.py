from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..authentication import admin_access
from ..database import get_db
from ..models import User
from ..schemas import UserModel, Tokendata, userData

router = APIRouter(prefix="/users", tags=['Users'])


# to create a new user
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserModel, db: Session = Depends(get_db)):
    admin_access(new_user.token)
    user = User(name=new_user.name, city=new_user.city, age=new_user.age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return f"user Created and user unique id is {user.id}"


# to get all user or filter the user according to city or search the user name
@router.get("/", status_code=status.HTTP_200_OK,response_model=List[userData])
def get_users(admin_token: Tokendata, db: Session = Depends(get_db), limit: int = 10, skip: int = 0, name: str = "",
              city: str = ""):
    admin_access(admin_token.token)
    users = db.query(User).filter(User.name.contains(name), User.city.contains(city)).limit(limit).offset(skip).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sorry no users not found")
    return users


# to get a specific user with unique id
@router.get("/{idx}", status_code=status.HTTP_200_OK,response_model=userData)
def get_user(admin_token: Tokendata, idx: int, db: Session = Depends(get_db)):
    admin_access(admin_token.token)
    user = db.query(User).filter(User.id == idx).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sorry user with id {idx} not found")
    return user


# to update the user
@router.put("/{idx}", status_code=status.HTTP_202_ACCEPTED,response_model=userData)
def update_user(new_user: UserModel, idx: int, db: Session = Depends(get_db)):
    admin_access(new_user.token)
    user_query = db.query(User).filter(User.id == idx)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sorry user with id {idx} not found")
    new_user = new_user.dict()
    new_user.pop('token')
    user_query.update(new_user, synchronize_session=False)
    db.commit()
    return user_query.first()


# to delete user
@router.delete("/{idx}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(admin_token: Tokendata, idx: int, db: Session = Depends(get_db)):
    admin_access(admin_token.token)
    user_query = db.query(User).filter(User.id == idx)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sorry user with id {idx} not found")
    user_query.delete(synchronize_session=False)
    db.commit()
    return "User Deleted Successfully"
