<template>
  <div class="app-container">
    <!-- Sidebar - Left -->
    <aside class="sidebar">
      <Sidebar />
    </aside>

    <!-- Main Content Area -->
    <div class="main-content">
      <!-- Three.js Viewer - Takes most of the space -->
      <div class="viewer-container">
        <ThreeViewer />
      </div>
      
      <!-- Bottom Panel -->
      <div class="bottom-panel">
        <BottomPanel />
      </div>
    </div>
  </div>
</template>

<script setup>
import ThreeViewer from './components/ThreeViewer.vue'
import Sidebar from './components/Sidebar.vue'
import BottomPanel from './components/BottomPanel.vue'
</script>

<style scoped>
.app-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Sidebar Styles */
.sidebar {
  width: 250px;
  background-color: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

/* Main Content Area (right of sidebar) */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Three.js Viewer Container */
.viewer-container {
  flex: 1;
  position: relative;
  background-color: #111122;
  overflow: hidden;
}

/* Bottom Panel */
.bottom-panel {
  background-color: #ecf0f1;
  overflow-y: auto;
  z-index: 5;
}

/* Responsive Design - Mobile */
@media (max-width: 768px) {
  .sidebar {
    width: 200px;
  }
  
  .bottom-panel {
    height: 150px;
  }
}

/* Scrollbar Styling */
.bottom-panel::-webkit-scrollbar {
  width: 8px;
}

.bottom-panel::-webkit-scrollbar-track {
  background: #d5d8dc;
}

.bottom-panel::-webkit-scrollbar-thumb {
  background: #95a5a6;
  border-radius: 4px;
}

.bottom-panel::-webkit-scrollbar-thumb:hover {
  background: #7f8c8d;
}
</style>