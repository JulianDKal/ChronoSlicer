<template>
  <div class="bottom-panel-container">
    
    <div class="panel-content">
      <div class="two-column-layout">
        <!-- Left Column: PlayBack Component (70%) -->
        <div class="playback-column">
          <PlayBack />
        </div>
        
        <!-- Right Column: Download Component (30%) -->
        <div class="download-column">
          <DownloadComponent ref="downloadComponentRef" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PlayBack from './PlayBack.vue'
import DownloadComponent from './DownloadComponent.vue'

const downloadComponentRef = ref(null)

// Optional: Method to update download time from parent
const updateDownloadTime = (seconds) => {
  if (downloadComponentRef.value) {
    downloadComponentRef.value.updateTime(seconds)
  }
}

// Expose methods to parent if needed
defineExpose({
  updateDownloadTime
})
</script>

<style scoped>
.bottom-panel-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
}

.collapse-btn {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.panel-content {
  flex: 1;
  padding: 15px;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* Two Column Layout - 70% / 30% Split */
.two-column-layout {
  display: flex;
  gap: 15px;
  justify-content: center;
  height: 100%;
  width: 100%;
}

.playback-column {
  flex: 7; /* 70% of the space */
  min-width: 0; /* Prevents overflow */
  background: #fafbfc;
  border-radius: 8px;
  overflow: auto;
}

.download-column {
  flex: 3; /* 30% of the space */
  min-width: 0; /* Prevents overflow */
}

/* Scrollbar styling for playback column */
.playback-column::-webkit-scrollbar {
  width: 6px;
}

.playback-column::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.playback-column::-webkit-scrollbar-thumb {
  background: #bdc3c7;
  border-radius: 3px;
}

.playback-column::-webkit-scrollbar-thumb:hover {
  background: #95a5a6;
}

/* Responsive: Stack vertically on small screens */
@media (max-width: 768px) {
  .two-column-layout {
    flex-direction: column;
  }
  
  .playback-column,
  .download-column {
    flex: 1;
  }
  
  .download-column {
    min-height: 200px;
  }
}
</style>