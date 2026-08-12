<script lang="ts">
  import { isDarkMode, isHighContrast, isLargeText } from '../lib/stores';
  
  function toggleDarkMode() {
    isDarkMode.update(v => !v);
  }
  
  function toggleHighContrast() {
    isHighContrast.update(v => !v);
  }
  
  function toggleLargeText() {
    isLargeText.update(v => !v);
  }
</script>

<div class="fixed top-4 right-4 flex gap-2 z-50">
  <button
    on:click={toggleDarkMode}
    class="p-3 rounded-full glass-card hover:scale-110 transition-transform"
    title="Toggle dark mode"
    aria-label="Toggle dark mode"
  >
    {#if $isDarkMode}
      ☀️
    {:else}
      🌙
    {/if}
  </button>
  
  <button
    on:click={toggleHighContrast}
    class="p-3 rounded-full glass-card hover:scale-110 transition-transform"
    title="Toggle high contrast"
    aria-label="Toggle high contrast"
  >
    👁️
  </button>
  
  <button
    on:click={toggleLargeText}
    class="p-3 rounded-full glass-card hover:scale-110 transition-transform"
    title="Toggle large text"
    aria-label="Toggle large text"
  >
    🔤
  </button>
</div>
