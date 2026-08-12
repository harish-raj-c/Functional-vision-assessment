<script lang="ts">
  import { onMount } from 'svelte';
  import { currentScreen, assessmentResults } from '../lib/stores';
  import { api } from '../lib/api';

  let results: any = null;
  let downloading = false;

  onMount(async () => {
    try {
      results = await api.getResults();
      assessmentResults.set(results);
    } catch (error) {
      console.error('Failed to get results:', error);
    }
  });

  async function downloadPDF() {
    downloading = true;
    try {
      const blob = await api.getResultsPDF();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `functional-vision-assessment-${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to download PDF:', error);
    } finally {
      downloading = false;
    }
  }

  async function downloadCSV() {
    try {
      const csv = await api.getResultsCSV();
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `functional-vision-assessment-${new Date().toISOString().split('T')[0]}.csv`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to download CSV:', error);
    }
  }

  function getScoreColor(score: number) {
    if (score >= 85) return 'text-green-600 dark:text-green-400';
    if (score >= 70) return 'text-blue-600 dark:text-blue-400';
    if (score >= 55) return 'text-yellow-600 dark:text-yellow-400';
    if (score >= 40) return 'text-orange-600 dark:text-orange-400';
    return 'text-red-600 dark:text-red-400';
  }

  function getPerformanceColor(summary: string) {
    if (summary === 'Excellent') return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400';
    if (summary === 'Good') return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400';
    if (summary === 'Fair') return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400';
    if (summary === 'Needs Improvement') return 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400';
    return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400';
  }
</script>

<div class="max-w-4xl mx-auto animate-fade-in">
  {#if results}
    <div class="glass-card p-10">
      <h2 class="text-4xl font-bold text-gray-800 dark:text-white mb-8 text-center">
        Assessment Results
      </h2>
      
      <!-- Score Circle -->
      <div class="flex justify-center mb-10">
        <div class="relative w-48 h-48">
          <svg class="w-full h-full transform -rotate-90">
            <circle
              cx="96"
              cy="96"
              r="88"
              stroke="currentColor"
              stroke-width="12"
              fill="none"
              class="text-gray-200 dark:text-gray-700"
            />
            <circle
              cx="96"
              cy="96"
              r="88"
              stroke="currentColor"
              stroke-width="12"
              fill="none"
              stroke-dasharray="{2 * Math.PI * 88}"
              stroke-dashoffset="{2 * Math.PI * 88 * (1 - results.functional_vision_score / 100)}"
              class="text-primary-500 transition-all duration-1000"
              style="transition: stroke-dashoffset 1s ease-in-out;"
            />
          </svg>
          <div class="absolute inset-0 flex flex-col items-center justify-center">
            <span class="text-5xl font-bold {getScoreColor(results.functional_vision_score)}">
              {results.functional_vision_score}
            </span>
            <span class="text-sm text-gray-600 dark:text-gray-400">Score</span>
          </div>
        </div>
      </div>
      
      <!-- Performance Summary -->
      <div class="text-center mb-8">
        <span class="inline-block px-6 py-3 rounded-full text-lg font-medium {getPerformanceColor(results.performance_summary)}">
          {results.performance_summary}
        </span>
      </div>
      
      <!-- Metrics Grid -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Accuracy</p>
          <p class="text-2xl font-bold text-gray-800 dark:text-white">
            {results.overall_accuracy.toFixed(1)}%
          </p>
        </div>
        
        <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg Response</p>
          <p class="text-2xl font-bold text-gray-800 dark:text-white">
            {results.average_response_time_ms.toFixed(0)}ms
          </p>
        </div>
        
        <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Fastest</p>
          <p class="text-2xl font-bold text-gray-800 dark:text-white">
            {results.fastest_response_ms.toFixed(0)}ms
          </p>
        </div>
        
        <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl text-center">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-1">Objects Detected</p>
          <p class="text-2xl font-bold text-gray-800 dark:text-white">
            {results.objects_detected}
          </p>
        </div>
      </div>
      
      <!-- Recommendation -->
      <div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-xl mb-8">
        <h3 class="font-semibold text-lg mb-2 text-blue-700 dark:text-blue-400">Recommendation</h3>
        <p class="text-gray-700 dark:text-gray-300">
          {results.recommendation}
        </p>
      </div>
      
      <!-- Level Results -->
      <div class="mb-8">
        <h3 class="text-xl font-bold text-gray-800 dark:text-white mb-4">Level-by-Level Results</h3>
        <div class="space-y-3">
          {#each results.level_results as levelResult}
            <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl">
              <div class="flex justify-between items-center mb-2">
                <span class="font-medium text-gray-800 dark:text-white">Level {levelResult.level}</span>
                <span class="text-sm text-gray-600 dark:text-gray-400">
                  {levelResult.scenes_completed}/{levelResult.total_scenes} scenes
                </span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600 dark:text-gray-400">
                  Accuracy: {levelResult.accuracy.toFixed(1)}%
                </span>
                <span class="text-sm text-gray-600 dark:text-gray-400">
                  Avg Time: {levelResult.average_response_time_ms.toFixed(0)}ms
                </span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2 mt-2">
                <div 
                  class="bg-primary-500 h-2 rounded-full"
                  style="width: {levelResult.accuracy}%"
                ></div>
              </div>
            </div>
          {/each}
        </div>
      </div>
      
      <!-- Download Buttons -->
      <div class="flex flex-wrap gap-4 justify-center mb-8">
        <button
          on:click={downloadPDF}
          disabled={downloading}
          class="healthcare-button-secondary flex items-center gap-2"
        >
          {#if downloading}
            <span class="animate-spin">⏳</span>
          {:else}
            📄
          {/if}
          Download PDF
        </button>
        
        <button
          on:click={downloadCSV}
          class="healthcare-button-secondary flex items-center gap-2"
        >
          📊
          Download CSV
        </button>
      </div>
      
      <!-- Navigation -->
      <div class="flex justify-center">
        <button
          on:click={() => currentScreen.set('home')}
          class="healthcare-button-primary"
        >
          Return to Home
        </button>
      </div>
    </div>
  {:else}
    <div class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">Loading results...</p>
    </div>
  {/if}
</div>
