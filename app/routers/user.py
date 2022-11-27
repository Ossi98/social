from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    tags=['Users'],
)


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash password
    hashed_pwd = utils.hash_pwd(user.password)
    user.password = hashed_pwd

    try:
        cuser = models.User(**user.dict())
        db.add(cuser)
        db.commit()
        db.refresh(cuser)
    except Exception:
        # if cuser is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return cuser


@router.get("/users/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id : {id} does not exist")

    return user
