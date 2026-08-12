from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NATS_URL: str = "nats://192.168.0.186:4222"

    # NATS Topics
    NATS_FACE_TOPIC: str = "vision.eye.cam0.face"
    NATS_DEPTH_TOPIC: str = "vision.eye.cam0.depth"
    NATS_BLINK_TOPIC: str = "vision.eye.cam0.blink"
    
    # Calibration thresholds
    MIN_DISTANCE_CM: float = 120.0
    MAX_DISTANCE_CM: float = 240.0
    POSITION_TOLERANCE: float = 0.3  # 30% from center
    
    # Assessment settings
    MAX_LEVELS: int = 5
    PRACTICE_ROUNDS: int = 1
    
    class Config:
        env_file = ".env"

settings = Settings()
