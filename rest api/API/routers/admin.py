from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, authentication
from ..database import get_db

router = APIRouter(tags=['Admin'])


@router.post('/login',status_code=status.HTTP_200_OK)
def login(user_credentials: schemas.admindata, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == user_credentials.email).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    if not utils.verify(user_credentials.password, admin.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid Credentials")

    token = authentication.create_access_token(data={"email": admin.email})

    return {"access_token": token}


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup_admin(new_admin: schemas.NewAdmin, db: Session = Depends(get_db)):
    check_admin = db.query(models.Admin).filter(models.Admin.email == new_admin.email).first()
    if check_admin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The admin with this email id already exists")

    new_admin.password = utils.hash(new_admin.password)

    admin = models.Admin(**new_admin.dict())
    db.add(admin)
    db.commit()
    return "Account created"
