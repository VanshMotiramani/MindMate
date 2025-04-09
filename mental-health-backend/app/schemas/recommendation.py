from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    user_id: int
    exercises: list[str] #["Deep breatingh", "Song"]
    songs: list[str]
