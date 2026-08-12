<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { currentScreen, sceneConfig, isPaused, pauseReason } from '../lib/stores';
  import { api } from '../lib/api';
  import { getObjectSVG } from '../lib/svg-objects';
  import { voiceRecognition } from '../lib/voice-recognition';
  import { keyboardInput } from '../lib/keyboard-input';

  let scene: any = null;
  let userAnswer = 0;
  let timeLeft = 0;
  let timerInterval: number;
  let visionInterval: number;
  let startTime = 0;
  let currentLevel = '1';
  let sceneIndex = 0;
  let scenesPerLevel = 3;
  let isVoiceEnabled = false;

  onMount(async () => {
    await loadScene();
    startVisionMonitoring();
    setupInputMethods();
  });

  onDestroy(() => {
    if (timerInterval) clearInterval(timerInterval);
    if (visionInterval) clearInterval(visionInterval);
    voiceRecognition.stop();
    keyboardInput.removeCallback();
  });

  function setupInputMethods() {
    // Voice recognition
    if (voiceRecognition.isSupported()) {
      voiceRecognition.start((transcript) => {
        const number = voiceRecognition.extractNumber(transcript);
        if (number !== null && !$isPaused) {
          submitAnswer(number);
        }
      });
    }

    // Keyboard input
    keyboardInput.setCallback((key) => {
      const number = keyboardInput.extractNumber(key);
      if (number !== null && !$isPaused) {
        submitAnswer(number);
      }
    });
  }

  async function loadScene() {
    try {
      scene = await api.getNextScene();
      sceneConfig.set(scene);
      if (scene) {
        startTime = Date.now();
        timeLeft = scene.time_limit_seconds;
        if (timeLeft > 0) {
          startTimer();
        }
      } else {
        // Assessment complete
        await finishAssessment();
      }
    } catch (error: unknown) {
      console.error('Failed to load scene:', error);
      if (error instanceof Error && error.message.includes('404')) {
        await finishAssessment();
      }
    }
  }

  function startTimer() {
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = window.setInterval(() => {
      if (timeLeft > 0 && !$isPaused) {
        timeLeft -= 1;
      } else if (timeLeft <= 0) {
        clearInterval(timerInterval);
        submitAnswer(0); // Time's up
      }
    }, 1000);
  }

  function startVisionMonitoring() {
    visionInterval = window.setInterval(async () => {
      try {
        const progress = await api.getProgress();
        currentLevel = progress.current_level || '1';
        sceneIndex = progress.scene_index;
        
        if (progress.is_paused && !$isPaused) {
          isPaused.set(true);
          pauseReason.set('Please return to the correct position.');
        } else if (!progress.is_paused && $isPaused) {
          isPaused.set(false);
        }
      } catch (error: any) {
        console.error('Failed to check progress:', error);
      }
    }, 500);
  }

  async function submitAnswer(answer: number) {
    if (timerInterval) clearInterval(timerInterval);
    
    try {
      await api.submitAnswer(answer);
      await loadScene();
    } catch (error: any) {
      console.error('Failed to submit answer:', error);
    }
  }

  async function finishAssessment() {
    if (timerInterval) clearInterval(timerInterval);
    if (visionInterval) clearInterval(visionInterval);
    
    try {
      const results = await api.getResults();
      currentScreen.set('results');
    } catch (error: any) {
      console.error('Failed to get results:', error);
    }
  }
</script>

<div class="max-w-4xl mx-auto animate-fade-in">
  <div class="glass-card p-8">
    <!-- Progress Bar -->
    <div class="mb-6">
      <div class="flex justify-between items-center mb-2">
        <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
          Level {currentLevel}
        </span>
        <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
          Scene {sceneIndex} of {scenesPerLevel}
        </span>
      </div>
      <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
        <div 
          class="bg-primary-500 h-2 rounded-full transition-all duration-300"
          style="width: {(sceneIndex / scenesPerLevel) * 100}%"
        ></div>
      </div>
    </div>

    <!-- Timer -->
    {#if timeLeft > 0}
      <div class="text-center mb-4">
        <span class="inline-flex items-center gap-2 bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400 px-4 py-2 rounded-full text-sm font-medium">
          ⏱️ {timeLeft}s
        </span>
      </div>
    {/if}

    <!-- Pause Overlay -->
    {#if $isPaused}
      <div class="absolute inset-0 bg-black/50 backdrop-blur-sm rounded-2xl flex items-center justify-center z-10">
        <div class="text-center p-8">
          <div class="text-6xl mb-4">⏸️</div>
          <p class="text-2xl font-bold text-white mb-2">Assessment Paused</p>
          <p class="text-gray-300">{$pauseReason}</p>
          <p class="text-sm text-gray-400 mt-4">Please return to the correct position to continue</p>
        </div>
      </div>
    {/if}

    {#if scene}
      <div class="text-center mb-6">
        <h3 class="text-2xl font-bold text-gray-800 dark:text-white mb-2">
          {scene.task_description}
        </h3>
      </div>
      
      <!-- Scene Display -->
      <div class="relative bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900/30 dark:to-purple-900/30 rounded-2xl h-96 mb-6 overflow-hidden">
        {#each scene.objects as obj}
          <div
            style="position: absolute; left: {obj.x * 100}%; top: {obj.y * 100}%; 
                   transform: translate(-50%, -50%) rotate({obj.rotation}deg) scale({obj.scale});"
            class="w-16 h-16"
          >
            {@html getObjectSVG(obj.type, obj.color)}
          </div>
        {/each}
      </div>
      
      <!-- Number Buttons -->
      <div class="grid grid-cols-5 gap-3 max-w-md mx-auto">
        {#each [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] as num}
          <button
            on:click={() => submitAnswer(num)}
            disabled={$isPaused}
            class="number-button bg-primary-500 hover:bg-primary-600 text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {num}
          </button>
        {/each}
      </div>
    {:else}
      <div class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-4 text-gray-600 dark:text-gray-400">Loading scene...</p>
      </div>
    {/if}
  </div>
</div>
