from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Level(str, Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"

class SceneType(str, Enum):
    PARK = "park"
    LIVING_ROOM = "living_room"
    KITCHEN = "kitchen"
    OFFICE = "office"
    BEDROOM = "bedroom"
    GARDEN = "garden"
    PLAYGROUND = "playground"

class ObjectType(str, Enum):
    BALLOON = "balloon"
    FOOTBALL = "football"
    BASKETBALL = "basketball"
    TEDDY_BEAR = "teddy_bear"
    CUP = "cup"
    BOTTLE = "bottle"
    APPLE = "apple"
    BOOK = "book"
    CHAIR = "chair"
    CLOCK = "clock"
    FLOWER = "flower"
    TOY_CAR = "toy_car"
    DOG = "dog"
    CAT = "cat"
    GIFT_BOX = "gift_box"
    PLANT = "plant"

class ObjectConfig(BaseModel):
    type: ObjectType
    x: float
    y: float
    scale: float
    rotation: float
    color: Optional[str] = None

class SceneConfig(BaseModel):
    scene_type: SceneType
    objects: List[ObjectConfig]
    target_object: ObjectType
    target_count: int
    task_description: str
    level: Level
    time_limit_seconds: int

class AssessmentResponse(BaseModel):
    user_answer: int
    correct_answer: int
    response_time_ms: float
    timestamp: datetime

class LevelResult(BaseModel):
    level: Level
    scenes_completed: int
    total_scenes: int
    correct_answers: int
    total_answers: int
    average_response_time_ms: float
    accuracy: float

class AssessmentResult(BaseModel):
    session_id: str
    functional_vision_score: float
    overall_accuracy: float
    average_response_time_ms: float
    fastest_response_ms: float
    objects_detected: int
    levels_completed: int
    level_results: List[LevelResult]
    performance_summary: str
    recommendation: str
    timestamp: datetime
