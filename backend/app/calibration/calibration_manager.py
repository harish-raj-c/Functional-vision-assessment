import asyncio
import logging
from typing import Optional, Callable
from datetime import datetime

from app.nats.nats_subscriber import NATSSubscriber
from app.models.vision import VisionState
from app.config import settings

logger = logging.getLogger(__name__)

class CalibrationManager:
    def __init__(self, nats_subscriber: NATSSubscriber):
        self.nats_subscriber = nats_subscriber
        self.is_calibrating = False
        self.calibration_callback: Optional[Callable] = None
        self._monitor_task: Optional[asyncio.Task] = None

    async def start_calibration(self, callback: Optional[Callable] = None):
        """Start calibration monitoring"""
        self.is_calibrating = True
        self.calibration_callback = callback
        self._monitor_task = asyncio.create_task(self._monitor_calibration())
        logger.info("Calibration monitoring started")

    async def stop_calibration(self):
        """Stop calibration monitoring"""
        self.is_calibrating = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("Calibration monitoring stopped")

    async def _monitor_calibration(self):
        """Continuously monitor vision state during calibration"""
        while self.is_calibrating:
            state = self.nats_subscriber.get_vision_state()
            
            if self.calibration_callback:
                try:
                    await self.calibration_callback(state)
                except Exception as e:
                    logger.error(f"Error in calibration callback: {e}")
            
            await asyncio.sleep(0.1)  # 10Hz update rate

    def get_calibration_status(self) -> dict:
        """Get current calibration status"""
        state = self.nats_subscriber.get_vision_state()
        
        return {
            "face_detected": state.face_detected,
            "distance_cm": state.distance_cm,
            "position_centered": state.position_centered,
            "distance_valid": (
                settings.MIN_DISTANCE_CM <= state.distance_cm <= settings.MAX_DISTANCE_CM
                if state.distance_cm else False
            ),
            "stable": state.stable,
            "timestamp": state.timestamp.isoformat()
        }

    def is_calibrated(self) -> bool:
        """Check if user is properly calibrated"""
        return self.nats_subscriber.is_calibrated()
