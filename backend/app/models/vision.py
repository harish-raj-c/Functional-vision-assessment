from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FaceDetection(BaseModel):
    detected: bool
    bounding_box: Optional[list[float]] = None  # [x, y, width, height]
    confidence: Optional[float] = None
    timestamp: datetime

class DepthData(BaseModel):
    distance_cm: float
    timestamp: datetime

class BlinkData(BaseModel):
    blinking: bool
    timestamp: datetime

class VisionState(BaseModel):
    face_detected: bool
    distance_cm: Optional[float] = None
    position_centered: bool
    stable: bool
    timestamp: datetime
