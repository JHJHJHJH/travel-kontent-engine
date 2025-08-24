from typing import List
from pydantic import BaseModel, Field

class Result(BaseModel):
    id: int
    scene: str
    image_prompt: str
    image_path: str
    video_prompt: str
    video_path: str

    def __init__(self):
        pass