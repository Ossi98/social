from fastapi import FastAPI


from app import models
from app.database import engine
from .routers import post, user, auth, vote


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}
