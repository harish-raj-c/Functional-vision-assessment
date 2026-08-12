import uuid
from typing import List
from datetime import datetime
from statistics import mean

from app.models.assessment import (
    AssessmentResponse, LevelResult, AssessmentResult, Level
)

class ScoreEngine:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.responses: List[AssessmentResponse] = []
        self.level_responses: dict[Level, List[AssessmentResponse]] = {
            Level.ONE: [],
            Level.TWO: [],
            Level.THREE: [],
            Level.FOUR: [],
            Level.FIVE: []
        }

    def add_response(self, response: AssessmentResponse, level: Level):
        """Add a response to the score engine"""
        self.responses.append(response)
        self.level_responses[level].append(response)

    def calculate_level_result(self, level: Level, scenes_per_level: int) -> LevelResult:
        """Calculate results for a specific level"""
        level_responses = self.level_responses[level]
        
        if not level_responses:
            return LevelResult(
                level=level,
                scenes_completed=0,
                total_scenes=scenes_per_level,
                correct_answers=0,
                total_answers=0,
                average_response_time_ms=0.0,
                accuracy=0.0
            )
        
        correct_answers = sum(1 for r in level_responses if r.user_answer == r.correct_answer)
        total_answers = len(level_responses)
        accuracy = (correct_answers / total_answers) * 100 if total_answers > 0 else 0.0
        avg_response_time = mean(r.response_time_ms for r in level_responses)
        
        return LevelResult(
            level=level,
            scenes_completed=total_answers,
            total_scenes=scenes_per_level,
            correct_answers=correct_answers,
            total_answers=total_answers,
            average_response_time_ms=avg_response_time,
            accuracy=accuracy
        )

    def calculate_final_score(self, scenes_per_level: int = 3) -> AssessmentResult:
        """Calculate the final functional vision score"""
        if not self.responses:
            return self._empty_result()
        
        # Calculate level results
        level_results = []
        for level in Level:
            level_results.append(self.calculate_level_result(level, scenes_per_level))
        
        # Overall metrics
        total_correct = sum(lr.correct_answers for lr in level_results)
        total_answers = sum(lr.total_answers for lr in level_results)
        overall_accuracy = (total_correct / total_answers) * 100 if total_answers > 0 else 0.0
        
        response_times = [r.response_time_ms for r in self.responses]
        average_response_time = mean(response_times) if response_times else 0.0
        fastest_response = min(response_times) if response_times else 0.0
        
        objects_detected = total_correct
        levels_completed = sum(1 for lr in level_results if lr.scenes_completed > 0)
        
        # Calculate functional vision score (0-100)
        # Weighted: accuracy (60%), speed (20%), level completion (20%)
        accuracy_score = overall_accuracy
        speed_score = max(0, 100 - (average_response_time / 50))  # 50ms = 0 score, 0ms = 100
        completion_score = (levels_completed / len(Level)) * 100
        
        functional_vision_score = (
            (accuracy_score * 0.6) +
            (speed_score * 0.2) +
            (completion_score * 0.2)
        )
        functional_vision_score = max(0, min(100, functional_vision_score))
        
        # Determine performance summary and recommendation
        performance_summary, recommendation = self._get_performance_summary(functional_vision_score)
        
        return AssessmentResult(
            session_id=self.session_id,
            functional_vision_score=round(functional_vision_score, 1),
            overall_accuracy=round(overall_accuracy, 1),
            average_response_time_ms=round(average_response_time, 1),
            fastest_response_ms=round(fastest_response, 1),
            objects_detected=objects_detected,
            levels_completed=levels_completed,
            level_results=level_results,
            performance_summary=performance_summary,
            recommendation=recommendation,
            timestamp=datetime.now()
        )

    def _empty_result(self) -> AssessmentResult:
        """Return an empty result when no responses recorded"""
        return AssessmentResult(
            session_id=self.session_id,
            functional_vision_score=0.0,
            overall_accuracy=0.0,
            average_response_time_ms=0.0,
            fastest_response_ms=0.0,
            objects_detected=0,
            levels_completed=0,
            level_results=[],
            performance_summary="No Data",
            recommendation="Please complete the assessment",
            timestamp=datetime.now()
        )

    def _get_performance_summary(self, score: float) -> tuple[str, str]:
        """Get performance summary and recommendation based on score"""
        if score >= 85:
            return "Excellent", "Your functional vision is excellent. Continue regular monitoring."
        elif score >= 70:
            return "Good", "Your functional vision is good. Maintain regular eye check-ups."
        elif score >= 55:
            return "Fair", "Your functional vision is fair. Consider consulting an eye specialist."
        elif score >= 40:
            return "Needs Improvement", "Your functional vision needs improvement. Please consult an eye specialist."
        else:
            return "Poor", "Your functional vision indicates significant difficulty. Please consult an eye specialist soon."

    def reset(self):
        """Reset the score engine for a new session"""
        self.session_id = str(uuid.uuid4())
        self.responses = []
        self.level_responses = {
            Level.ONE: [],
            Level.TWO: [],
            Level.THREE: [],
            Level.FOUR: [],
            Level.FIVE: []
        }
