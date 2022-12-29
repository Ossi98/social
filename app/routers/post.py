from typing import List, Optional

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, ouath2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
)


@router.get("", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(ouath2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post).filter(models.Post.published, models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_posts_by_id(id: int, db: Session = Depends(get_db),
                    current_user: models.User = Depends(ouath2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id, models.Post.owner_id == current_user.id).first()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not Found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(ouath2.get_current_user)):
    up_post = db.query(models.Post).filter(models.Post.id == id)

    if up_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    if up_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    up_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return up_post.first()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(ouath2.get_current_user)):
    cpost = models.Post(owner_id=current_user.id, **post.dict())
    db.add(cpost)
    db.commit()
    db.refresh(cpost)

    if cpost is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")

    return cpost


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(ouath2.get_current_user)):
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    post = delete_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    delete_query.delete(synchronize_session=False)
    db.commit()
