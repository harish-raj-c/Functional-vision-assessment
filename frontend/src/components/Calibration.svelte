<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { currentScreen, calibrationStatus } from '../lib/stores';
  import { api } from '../lib/api';

  let interval: number;
  let status = {
    face_detected: false,
    distance_cm: null as number | null,
    position_centered: false,
    distance_valid: false,
    stable: false
  };

  onMount(async () => {
    // Start polling calibration status
    interval = window.setInterval(async () => {
      try {
        const data = await api.getCalibrationStatus();
        status = data;
        calibrationStatus.set(data);
      } catch (error) {
        console.error('Failed to get calibration status:', error);
      }
    }, 200);
  });

  onDestroy(() => {
    if (interval) clearInterval(interval);
  });

  async function handleStart() {
    try {
      await api.startAssessment();
      currentScreen.set('practice');
    } catch (error) {
      console.error('Failed to start assessment:', error);
    }
  }
  
  function goBack() {
    currentScreen.set('instructions');
  }

  $: isCalibrated = status.face_detected && status.position_centered && status.distance_valid;
</script>

<div class="max-w-2xl mx-auto animate-fade-in">
  <div class="glass-card p-10">
    <h2 class="text-4xl font-bold text-gray-800 dark:text-white mb-6 text-center">
      Calibration
    </h2>
    
    <p class="text-lg text-gray-600 dark:text-gray-300 text-center mb-8">
      Please position yourself in front of the camera. We need to verify your position before starting.
    </p>
    
    <div class="grid grid-cols-2 gap-4 mb-8">
      <div class="status-indicator {status.face_detected ? 'status-success' : 'status-pending'}">
        <span>{status.face_detected ? '✓' : '○'}</span>
        <span>Face Detected</span>
      </div>
      
      <div class="status-indicator {status.position_centered ? 'status-success' : 'status-pending'}">
        <span>{status.position_centered ? '✓' : '○'}</span>
        <span>Position Centered</span>
      </div>
      
      <div class="status-indicator {status.distance_valid ? 'status-success' : 'status-warning'}">
        <span>{status.distance_valid ? '✓' : '○'}</span>
        <span>Distance: {status.distance_cm ? status.distance_cm.toFixed(0) : '--'} cm</span>
      </div>
      
      <div class="status-indicator {isCalibrated ? 'status-success' : 'status-pending'}">
        <span>{isCalibrated ? '✓' : '○'}</span>
        <span>Ready</span>
      </div>
    </div>
    
    <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-xl mb-8 text-center">
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Acceptable distance: 120-240 cm from camera
      </p>
    </div>
    
    <div class="flex gap-4 justify-center">
      <button
        on:click={goBack}
        class="healthcare-button-secondary"
      >
        Back
      </button>
      <button
        on:click={handleStart}
        disabled={!isCalibrated}
        class="healthcare-button-primary"
      >
        Start Practice Round
      </button>
    </div>
  </div>
</div>
