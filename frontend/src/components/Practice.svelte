<script lang="ts">
  import { onMount } from 'svelte';
  import { currentScreen, sceneConfig } from '../lib/stores';
  import { api } from '../lib/api';
  import { getObjectSVG } from '../lib/svg-objects';

  let scene: any = null;
  let userAnswer = 0;
  let showFeedback = false;
  let isCorrect = false;
  let startTime = 0;

  onMount(async () => {
    try {
      scene = await api.getNextScene();
      sceneConfig.set(scene);
      startTime = Date.now();
    } catch (error) {
      console.error('Failed to load practice scene:', error);
    }
  });

  async function submitAnswer(answer: number) {
    userAnswer = answer;
    const responseTime = Date.now() - startTime;
    
    try {
      const response = await api.submitAnswer(answer);
      isCorrect = response.user_answer === response.correct_answer;
      showFeedback = true;
      
      setTimeout(() => {
        currentScreen.set('assessment');
      }, 2000);
    } catch (error) {
      console.error('Failed to submit answer:', error);
    }
  }
</script>

<div class="max-w-4xl mx-auto animate-fade-in">
  <div class="glass-card p-8">
    <div class="text-center mb-6">
      <span class="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 px-4 py-2 rounded-full text-sm font-medium">
        Practice Round - No Scoring
      </span>
    </div>
    
    {#if scene}
      <div class="text-center mb-6">
        <h3 class="text-2xl font-bold text-gray-800 dark:text-white mb-2">
          {scene.task_description}
        </h3>
      </div>
      
      <div class="relative bg-gradient-to-br from-green-100 to-blue-100 dark:from-green-900/30 dark:to-blue-900/30 rounded-2xl h-96 mb-6 overflow-hidden">
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
      
      {#if !showFeedback}
        <div class="grid grid-cols-5 gap-3 max-w-md mx-auto">
          {#each [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] as num}
            <button
              on:click={() => submitAnswer(num)}
              class="number-button bg-primary-500 hover:bg-primary-600 text-white"
            >
              {num}
            </button>
          {/each}
        </div>
      {:else}
        <div class="text-center py-8">
          <div class="text-6xl mb-4">
            {isCorrect ? '✅' : '❌'}
          </div>
          <p class="text-2xl font-bold {isCorrect ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}">
            {isCorrect ? 'Correct!' : `The answer was ${scene.target_count}`}
          </p>
          <p class="text-gray-600 dark:text-gray-400 mt-2">
            Starting assessment...
          </p>
        </div>
      {/if}
    {:else}
      <div class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-4 text-gray-600 dark:text-gray-400">Loading practice scene...</p>
      </div>
    {/if}
  </div>
</div>
