
from fastapi import Depends, FastAPI

from . import models
from .database import engine
from .routes import user, sentiments, auth
import logging
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

# users_list: list[UserResponse] = []

# my_recommendations: dict[int, RecommendationResponse] = {
#     1: RecommendationResponse(user_id=1, exercises=["Deep breathing, Yoga"], songs=["Song A, Song B"]),
#     2: RecommendationResponse(user_id=2, exercises=["Meditation, Stretching"], songs=["Song C, Song D"]),
#     3: RecommendationResponse(user_id=3, exercises=["Progressive muscle relaxations"], songs=["Song E, SongF"])
# }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(sentiments.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Up and running!"}


# def get_recommendation(user_sentiment: str):
#     recommendation = model.predict([user_sentiment])
#     return recommendation[0]



