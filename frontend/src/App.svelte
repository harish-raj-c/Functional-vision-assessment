<script lang="ts">
  import { onMount } from 'svelte';
  import { currentScreen, isDarkMode, isHighContrast, isLargeText } from './lib/stores';
  import Home from './components/Home.svelte';
  import Instructions from './components/Instructions.svelte';
  import Calibration from './components/Calibration.svelte';
  import Practice from './components/Practice.svelte';
  import Assessment from './components/Assessment.svelte';
  import Results from './components/Results.svelte';
  import AccessibilityControls from './components/AccessibilityControls.svelte';

  onMount(() => {
    // Check system preference for dark mode
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      isDarkMode.set(true);
    }
  });

  $: document.documentElement.classList.toggle('dark', $isDarkMode);
  $: document.documentElement.classList.toggle('high-contrast', $isHighContrast);
  $: document.documentElement.classList.toggle('large-text', $isLargeText);
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 transition-colors duration-300">
  <AccessibilityControls />
  
  <main class="container mx-auto px-4 py-8 max-w-6xl">
    {#if $currentScreen === 'home'}
      <Home />
    {:else if $currentScreen === 'instructions'}
      <Instructions />
    {:else if $currentScreen === 'calibration'}
      <Calibration />
    {:else if $currentScreen === 'practice'}
      <Practice />
    {:else if $currentScreen === 'assessment'}
      <Assessment />
    {:else if $currentScreen === 'results'}
      <Results />
    {/if}
  </main>
</div>

<style>
  :global(.high-contrast) {
    filter: contrast(1.2);
  }
  
  :global(.large-text) {
    font-size: 120%;
  }
  
  :global(.large-text *) {
    font-size: inherit;
  }
</style>
