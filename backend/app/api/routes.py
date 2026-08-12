from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
import asyncio

from app.nats.nats_subscriber import NATSSubscriber
from app.calibration.calibration_manager import CalibrationManager
from app.assessment.assessment_controller import AssessmentController
from app.results.results_engine import ResultsEngine
from app.models.assessment import SceneConfig, AssessmentResponse, AssessmentResult
from app.models.vision import VisionState

router = APIRouter()

# Request models
class SubmitAnswerRequest(BaseModel):
    user_answer: int

# Global instances - will be initialized in main.py
nats_subscriber: NATSSubscriber = None
calibration_manager: CalibrationManager = None
assessment_controller: AssessmentController = None
results_engine: ResultsEngine = None

def init_instances(nats_sub: NATSSubscriber):
    """Initialize global instances with connected NATS subscriber"""
    global nats_subscriber, calibration_manager, assessment_controller, results_engine
    nats_subscriber = nats_sub
    calibration_manager = CalibrationManager(nats_subscriber)
    assessment_controller = AssessmentController(nats_subscriber)
    results_engine = ResultsEngine()

@router.get("/vision-state")
async def get_vision_state() -> VisionState:
    """Get current vision state from NATS"""
    return nats_subscriber.get_vision_state()

@router.get("/calibration-status")
async def get_calibration_status():
    """Get calibration status"""
    return calibration_manager.get_calibration_status()

@router.post("/assessment/start")
async def start_assessment():
    """Start the assessment"""
    await assessment_controller.start_assessment()
    return {"status": "started", "message": "Assessment started successfully"}

@router.post("/assessment/stop")
async def stop_assessment():
    """Stop the assessment"""
    await assessment_controller.stop_assessment()
    return {"status": "stopped", "message": "Assessment stopped"}

@router.get("/assessment/next-scene", response_model=Optional[SceneConfig])
async def get_next_scene():
    """Get the next scene in the assessment"""
    if assessment_controller.is_paused:
        raise HTTPException(status_code=400, detail="Assessment is paused")
    scene = await assessment_controller.get_next_scene()
    if not scene:
        raise HTTPException(status_code=404, detail="No more scenes available")
    return scene

@router.post("/assessment/submit-answer", response_model=AssessmentResponse)
async def submit_answer(request: SubmitAnswerRequest):
    """Submit answer for current scene"""
    if assessment_controller.is_paused:
        raise HTTPException(status_code=400, detail="Assessment is paused")
    try:
        response = await assessment_controller.submit_answer(request.user_answer)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/assessment/progress")
async def get_assessment_progress():
    """Get assessment progress"""
    return assessment_controller.get_scene_progress()

@router.get("/assessment/results", response_model=AssessmentResult)
async def get_assessment_results():
    """Get final assessment results"""
    return await assessment_controller.get_results()

@router.get("/assessment/results/json")
async def get_results_json():
    """Get results as JSON"""
    result = await assessment_controller.get_results()
    return results_engine.generate_json(result)

@router.get("/assessment/results/csv")
async def get_results_csv():
    """Get results as CSV"""
    result = await assessment_controller.get_results()
    csv_data = results_engine.generate_csv(result)
    return {"csv": csv_data}

@router.get("/assessment/results/pdf")
async def get_results_pdf():
    """Get results as PDF"""
    result = await assessment_controller.get_results()
    pdf_data = results_engine.generate_pdf(result)
    from fastapi.responses import Response
    return Response(content=pdf_data, media_type="application/pdf",
                    headers={"Content-Disposition": "attachment; filename=assessment_results.pdf"})

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "functional-vision-assessment-api"}
