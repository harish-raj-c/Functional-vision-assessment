<script lang="ts">
  import { currentScreen } from '../lib/stores';
  
  function startAssessment() {
    currentScreen.set('instructions');
  }
</script>

<div class="flex flex-col items-center justify-center min-h-[80vh] animate-fade-in">
  <div class="glass-card p-12 max-w-2xl text-center">
    <div class="mb-8">
      <h1 class="text-5xl font-bold text-gray-800 dark:text-white mb-4">
        Functional Vision Assessment
      </h1>
      <p class="text-2xl text-primary-600 dark:text-primary-400 font-medium">
        Find and Count Everyday Objects
      </p>
    </div>
    
    <div class="mb-10 text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
      <p class="mb-4">
        This assessment measures how well you detect and recognize everyday objects under different viewing conditions.
      </p>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        Duration: 2-3 minutes
      </p>
    </div>
    
    <button
      on:click={startAssessment}
      class="healthcare-button-primary text-xl px-12 py-5"
    >
      Start Assessment
    </button>
  </div>
</div>
