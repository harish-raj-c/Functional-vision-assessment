<script lang="ts">
  import { currentScreen } from '../lib/stores';
  
  function goBack() {
    currentScreen.set('home');
  }
  
  function goToCalibration() {
    currentScreen.set('calibration');
  }
</script>

<div class="max-w-3xl mx-auto animate-fade-in">
  <div class="glass-card p-10">
    <h2 class="text-4xl font-bold text-gray-800 dark:text-white mb-8 text-center">
      Instructions
    </h2>
    
    <div class="space-y-6 text-lg text-gray-700 dark:text-gray-300">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-xl">
        <h3 class="font-semibold text-xl mb-3 text-primary-700 dark:text-primary-400">
          What You'll Do
        </h3>
        <p>
          We will display several everyday objects on the screen. Your task is to count only the requested object type.
        </p>
      </div>
      
      <div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-xl">
        <h3 class="font-semibold text-xl mb-3 text-green-700 dark:text-green-400">
          How to Answer
        </h3>
        <p>
          Answer as accurately and as quickly as possible using the number buttons on the screen.
        </p>
      </div>
      
      <div class="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-xl">
        <h3 class="font-semibold text-xl mb-3 text-purple-700 dark:text-purple-400">
          Example
        </h3>
        <div class="flex items-center gap-4">
          <span class="text-4xl">🎈</span>
          <div>
            <p class="font-medium">Target: Balloon</p>
            <p class="text-gray-600 dark:text-gray-400">Question: How many balloons do you see?</p>
          </div>
        </div>
      </div>
      
      <div class="bg-orange-50 dark:bg-orange-900/20 p-6 rounded-xl">
        <h3 class="font-semibold text-xl mb-3 text-orange-700 dark:text-orange-400">
          Important Notes
        </h3>
        <ul class="list-disc list-inside space-y-2">
          <li>Stay in front of the camera throughout the assessment</li>
          <li>Keep your distance between 120-240 cm from the camera</li>
          <li>Answer before the timer runs out</li>
          <li>There are 5 levels with increasing difficulty</li>
        </ul>
      </div>
    </div>
    
    <div class="flex gap-4 mt-10 justify-center">
      <button
        on:click={goBack}
        class="healthcare-button-secondary"
      >
        Back
      </button>
      <button
        on:click={goToCalibration}
        class="healthcare-button-primary"
      >
        Continue to Calibration
      </button>
    </div>
  </div>
</div>
