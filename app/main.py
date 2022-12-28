from fastapi import FastAPI


from app import models
from app.database import engine
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root() -> dict:
    """    
    '''$2y$10$TwbInXyE4J/Hmi9gOIXySeWsOBfptzYQZgn.8qMxZLpyC4gFpVJLa = 123456'''
    user = models.User(email="test@test.com",password='$2y$10$TwbInXyE4J/Hmi9gOIXySeWsOBfptzYQZgn.8qMxZLpyC4gFpVJLa')
    db.add(user)
    db.commit()
    db.refresh(user)"""
    return {"message": "Hello World Mimi"}
