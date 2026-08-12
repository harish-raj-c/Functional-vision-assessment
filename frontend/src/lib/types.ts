export type Screen = 'home' | 'instructions' | 'calibration' | 'practice' | 'assessment' | 'results';

export interface VisionState {
  face_detected: boolean;
  distance_cm: number | null;
  position_centered: boolean;
  stable: boolean;
  timestamp: string;
}

export interface CalibrationStatus {
  face_detected: boolean;
  distance_cm: number | null;
  position_centered: boolean;
  distance_valid: boolean;
  stable: boolean;
  timestamp: string;
}

export interface ObjectConfig {
  type: string;
  x: number;
  y: number;
  scale: number;
  rotation: number;
  color?: string;
}

export interface SceneConfig {
  scene_type: string;
  objects: ObjectConfig[];
  target_object: string;
  target_count: number;
  task_description: string;
  level: string;
  time_limit_seconds: number;
}

export interface AssessmentResponse {
  user_answer: number;
  correct_answer: number;
  response_time_ms: number;
  timestamp: string;
}

export interface LevelResult {
  level: string;
  scenes_completed: number;
  total_scenes: number;
  correct_answers: number;
  total_answers: number;
  average_response_time_ms: number;
  accuracy: number;
}

export interface AssessmentResult {
  session_id: string;
  functional_vision_score: number;
  overall_accuracy: number;
  average_response_time_ms: number;
  fastest_response_ms: number;
  objects_detected: number;
  levels_completed: number;
  level_results: LevelResult[];
  performance_summary: string;
  recommendation: string;
  timestamp: string;
}

export interface SceneProgress {
  current_level: string | null;
  scene_index: number;
  scenes_per_level: number;
  is_paused: boolean;
}
