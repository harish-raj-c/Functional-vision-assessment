import type {
  VisionState,
  CalibrationStatus,
  SceneConfig,
  AssessmentResponse,
  AssessmentResult,
  SceneProgress
} from './types';

const API_BASE = '/api/v1';

async function fetchAPI(endpoint: string, options?: RequestInit) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers
    },
    ...options
  });
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }
  
  return response.json();
}

export const api = {
  // Vision
  async getVisionState(): Promise<VisionState> {
    return fetchAPI('/vision-state');
  },

  async getCalibrationStatus(): Promise<CalibrationStatus> {
    return fetchAPI('/calibration-status');
  },

  // Assessment
  async startAssessment(): Promise<{ status: string; message: string }> {
    return fetchAPI('/assessment/start', { method: 'POST' });
  },

  async stopAssessment(): Promise<{ status: string; message: string }> {
    return fetchAPI('/assessment/stop', { method: 'POST' });
  },

  async getNextScene(): Promise<SceneConfig> {
    return fetchAPI('/assessment/next-scene');
  },

  async submitAnswer(userAnswer: number): Promise<AssessmentResponse> {
    return fetchAPI('/assessment/submit-answer', {
      method: 'POST',
      body: JSON.stringify({ user_answer: userAnswer })
    });
  },

  async getProgress(): Promise<SceneProgress> {
    return fetchAPI('/assessment/progress');
  },

  async getResults(): Promise<AssessmentResult> {
    return fetchAPI('/assessment/results');
  },

  // Reports
  async getResultsJSON(): Promise<string> {
    const response = await fetch(`${API_BASE}/assessment/results/json`);
    return response.text();
  },

  async getResultsCSV(): Promise<string> {
    const response = await fetch(`${API_BASE}/assessment/results/csv`);
    const data = await response.json();
    return data.csv;
  },

  async getResultsPDF(): Promise<Blob> {
    const response = await fetch(`${API_BASE}/assessment/results/pdf`);
    return response.blob();
  },

  async healthCheck(): Promise<{ status: string; service: string }> {
    return fetchAPI('/health');
  }
};
