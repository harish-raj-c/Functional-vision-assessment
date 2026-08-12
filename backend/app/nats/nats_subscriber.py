import asyncio
import json
import logging
from datetime import datetime
from typing import Optional, Callable

import nats
from nats.js.api import StreamConfig, ConsumerConfig

from app.config import settings
from app.models.vision import FaceDetection, DepthData, BlinkData, VisionState

logger = logging.getLogger(__name__)

class NATSSubscriber:
    def __init__(self):
        self.nc: Optional[nats.aio.client.Client] = None
        self.js: Optional[nats.aio.client.JetStreamContext] = None
        self.current_face_data: Optional[FaceDetection] = None
        self.current_depth_data: Optional[DepthData] = None
        self.current_blink_data: Optional[BlinkData] = None
        self.callbacks: list[Callable] = []
        self._running = False

    async def connect(self):
        try:
            self.nc = await nats.connect(settings.NATS_URL)
            self.js = self.nc.jetstream()
            logger.info(f"Connected to NATS at {settings.NATS_URL}")
            
            # Subscribe to vision topics
            await self._subscribe_to_face()
            await self._subscribe_to_depth()
            await self._subscribe_to_blink()
            
            self._running = True
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")

    async def disconnect(self):
        self._running = False
        if self.nc:
            await self.nc.close()
            logger.info("Disconnected from NATS")

    async def _subscribe_to_face(self):
        async def face_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                logger.info(f"[FACE DATA] {data}")
                
                # Parse bbox from {x1, y1, x2, y2} to [x, y, width, height]
                bbox = None
                if 'bbox' in data and data['bbox']:
                    bbox_data = data['bbox']
                    bbox = [bbox_data.get('x1', 0), bbox_data.get('y1', 0), 
                            bbox_data.get('x2', 0) - bbox_data.get('x1', 0), 
                            bbox_data.get('y2', 0) - bbox_data.get('y1', 0)]
                
                self.current_face_data = FaceDetection(
                    detected=data.get('face_detected', False),
                    bounding_box=bbox,
                    confidence=None,  # Not provided in actual data
                    timestamp=datetime.now()
                )
                await self._notify_callbacks()
            except Exception as e:
                logger.error(f"Error processing face data: {e}")
        
        await self.nc.subscribe(settings.NATS_FACE_TOPIC, cb=face_handler)
        logger.info(f"Subscribed to {settings.NATS_FACE_TOPIC}")

    async def _subscribe_to_depth(self):
        async def depth_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                logger.info(f"[DEPTH DATA] {data}")
                
                # Use 'mean' field as distance_cm (appears to be in cm based on values ~175-180)
                distance_cm = data.get('mean', 0.0)
                
                self.current_depth_data = DepthData(
                    distance_cm=distance_cm,
                    timestamp=datetime.now()
                )
                await self._notify_callbacks()
            except Exception as e:
                logger.error(f"Error processing depth data: {e}")
        
        await self.nc.subscribe(settings.NATS_DEPTH_TOPIC, cb=depth_handler)
        logger.info(f"Subscribed to {settings.NATS_DEPTH_TOPIC}")

    async def _subscribe_to_blink(self):
        async def blink_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                logger.info(f"[BLINK DATA] {data}")
                self.current_blink_data = BlinkData(
                    blinking=data.get('blink', False),
                    timestamp=datetime.now()
                )
                await self._notify_callbacks()
            except Exception as e:
                logger.error(f"Error processing blink data: {e}")
        
        await self.nc.subscribe(settings.NATS_BLINK_TOPIC, cb=blink_handler)
        logger.info(f"Subscribed to {settings.NATS_BLINK_TOPIC}")

    async def _notify_callbacks(self):
        vision_state = self.get_vision_state()
        logger.info(f"[VISION STATE] face_detected={vision_state.face_detected}, distance_cm={vision_state.distance_cm}, position_centered={vision_state.position_centered}, stable={vision_state.stable}")
        for callback in self.callbacks:
            try:
                await callback(vision_state)
            except Exception as e:
                logger.error(f"Error in callback: {e}")

    def register_callback(self, callback: Callable):
        self.callbacks.append(callback)

    def unregister_callback(self, callback: Callable):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def get_vision_state(self) -> VisionState:
        face_detected = self.current_face_data.detected if self.current_face_data else False
        distance_cm = self.current_depth_data.distance_cm if self.current_depth_data else None
        
        # Check if position is centered (bounding box should be near center)
        position_centered = False
        if self.current_face_data and self.current_face_data.bounding_box:
            bbox = self.current_face_data.bounding_box
            # Bbox is in pixel coordinates [x, y, width, height]
            # Calculate face center
            face_center_x = bbox[0] + bbox[2] / 2
            face_center_y = bbox[1] + bbox[3] / 2
            
            # Normalize to 0-1 range by assuming max possible values
            # Use a large enough max (1920x1080) to handle most cameras
            normalized_x = face_center_x / 1920.0
            normalized_y = face_center_y / 1080.0
            
            # Center is 0.5, allow 40% tolerance (very lenient)
            position_centered = (
                0.1 <= normalized_x <= 0.9 and
                0.1 <= normalized_y <= 0.9
            )
            
            logger.info(f"[POSITION] face_center=({face_center_x}, {face_center_y}), normalized=({normalized_x:.2f}, {normalized_y:.2f}), centered={position_centered}")
        
        # Check if distance is within acceptable range
        distance_valid = False
        if distance_cm:
            distance_valid = settings.MIN_DISTANCE_CM <= distance_cm <= settings.MAX_DISTANCE_CM
            logger.info(f"[DISTANCE] cm={distance_cm:.1f}, valid={distance_valid}, range=[{settings.MIN_DISTANCE_CM}, {settings.MAX_DISTANCE_CM}]")
        
        stable = face_detected and position_centered and distance_valid
        
        logger.info(f"[STATE] face_detected={face_detected}, position_centered={position_centered}, distance_valid={distance_valid}, stable={stable}")
        
        return VisionState(
            face_detected=face_detected,
            distance_cm=distance_cm,
            position_centered=position_centered,
            stable=stable,
            timestamp=datetime.now()
        )

    def is_calibrated(self) -> bool:
        state = self.get_vision_state()
        return state.stable
