import { writable } from 'svelte/store';
import type { Screen, SceneConfig, AssessmentResult, CalibrationStatus } from './types';

export const currentScreen = writable<Screen>('home');
export const sceneConfig = writable<SceneConfig | null>(null);
export const assessmentResults = writable<AssessmentResult | null>(null);
export const calibrationStatus = writable<CalibrationStatus | null>(null);
export const isDarkMode = writable(false);
export const isHighContrast = writable(false);
export const isLargeText = writable(false);
export const isPaused = writable(false);
export const pauseReason = writable<string>('');
