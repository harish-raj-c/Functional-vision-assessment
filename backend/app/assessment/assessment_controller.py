import asyncio
import logging
from typing import Optional, Callable
from datetime import datetime

from app.nats.nats_subscriber import NATSSubscriber
from app.calibration.calibration_manager import CalibrationManager
from app.scene.scene_engine import SceneEngine
from app.score.score_engine import ScoreEngine
from app.models.assessment import (
    SceneConfig, AssessmentResponse, Level, AssessmentResult
)
from app.config import settings

logger = logging.getLogger(__name__)

class AssessmentController:
    def __init__(self, nats_subscriber: NATSSubscriber):
        self.nats_subscriber = nats_subscriber
        self.calibration_manager = CalibrationManager(nats_subscriber)
        self.scene_engine = SceneEngine()
        self.score_engine = ScoreEngine()
        
        self.is_running = False
        self.is_paused = False
        self.current_level: Optional[Level] = None
        self.current_scene: Optional[SceneConfig] = None
        self.scene_start_time: Optional[datetime] = None
        self.scenes_per_level = 3
        self.current_scene_index = 0
        
        self.pause_callback: Optional[Callable] = None
        self.resume_callback: Optional[Callable] = None
        self._monitor_task: Optional[asyncio.Task] = None

    async def start_assessment(self):
        """Start the assessment"""
        self.is_running = True
        self.is_paused = False
        self.current_level = Level.ONE
        self.current_scene_index = 0
        self.score_engine.reset()
        
        # Start live monitoring
        self._monitor_task = asyncio.create_task(self._monitor_vision_state())
        logger.info("Assessment started")

    async def stop_assessment(self):
        """Stop the assessment"""
        self.is_running = False
        self.is_paused = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("Assessment stopped")

    async def _monitor_vision_state(self):
        """Monitor vision state and pause if needed"""
        while self.is_running:
            if not self.is_paused:
                state = self.nats_subscriber.get_vision_state()
                
                if not state.stable:
                    await self._pause_assessment("Please return to the correct position.")
                elif self.is_paused and state.stable:
                    await self._resume_assessment()
            
            await asyncio.sleep(0.1)

    async def _pause_assessment(self, reason: str):
        """Pause the assessment"""
        if not self.is_paused:
            self.is_paused = True
            logger.info(f"Assessment paused: {reason}")
            if self.pause_callback:
                await self.pause_callback(reason)

    async def _resume_assessment(self):
        """Resume the assessment"""
        if self.is_paused:
            self.is_paused = False
            logger.info("Assessment resumed")
            if self.resume_callback:
                await self.resume_callback()

    def set_pause_callback(self, callback: Callable):
        """Set callback for pause events"""
        self.pause_callback = callback

    def set_resume_callback(self, callback: Callable):
        """Set callback for resume events"""
        self.resume_callback = callback

    async def get_next_scene(self) -> Optional[SceneConfig]:
        """Get the next scene for the assessment"""
        if self.is_paused:
            raise ValueError("Assessment is paused")
        
        # Initialize level if not set
        if not self.current_level:
            self.current_level = Level.ONE
            self.current_scene_index = 0
        
        # Check if we need to move to next level
        if self.current_scene_index >= self.scenes_per_level:
            current_level_value = int(self.current_level.value)
            if current_level_value < settings.MAX_LEVELS:
                self.current_level = Level(str(current_level_value + 1))
                self.current_scene_index = 0
                logger.info(f"Moving to level {self.current_level.value}")
            else:
                # Assessment complete
                logger.info("Assessment complete - all levels finished")
                return None
        
        self.current_scene = self.scene_engine.generate_scene(self.current_level)
        self.scene_start_time = datetime.now()
        self.current_scene_index += 1
        
        logger.info(f"Generated scene for level {self.current_level.value}, scene {self.current_scene_index}/{self.scenes_per_level}")
        return self.current_scene

    async def submit_answer(self, user_answer: int) -> AssessmentResponse:
        """Submit an answer for the current scene"""
        if not self.current_scene:
            raise ValueError("No active scene")
        
        response_time = (datetime.now() - self.scene_start_time).total_seconds() * 1000
        
        response = AssessmentResponse(
            user_answer=user_answer,
            correct_answer=self.current_scene.target_count,
            response_time_ms=response_time,
            timestamp=datetime.now()
        )
        
        self.score_engine.add_response(response, self.current_level)
        
        return response

    async def get_results(self) -> AssessmentResult:
        """Get the final assessment results"""
        return self.score_engine.calculate_final_score(self.scenes_per_level)

    def get_current_level(self) -> Optional[Level]:
        """Get the current level"""
        return self.current_level

    def get_scene_progress(self) -> dict:
        """Get progress through current level"""
        return {
            "current_level": self.current_level.value if self.current_level else None,
            "scene_index": self.current_scene_index,
            "scenes_per_level": self.scenes_per_level,
            "is_paused": self.is_paused
        }

    def is_assessment_complete(self) -> bool:
        """Check if assessment is complete"""
        if not self.current_level:
            return False
        return (
            int(self.current_level.value) > settings.MAX_LEVELS or
            (self.current_scene_index >= self.scenes_per_level and 
             int(self.current_level.value) == settings.MAX_LEVELS)
        )
