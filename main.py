from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from view.user_router import user_router
from view.genre_router import genre_router
from view.movie_router import movie_router
from view.review_router import review_router
from view.like_router import like_router
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": f"internal database error: {exc}"}
    )

app.include_router(user_router)
app.include_router(genre_router)
app.include_router(movie_router)
app.include_router(review_router)
app.include_router(like_router)

@app.get('/')
def root():
    return {'message': "Hello world!"}
