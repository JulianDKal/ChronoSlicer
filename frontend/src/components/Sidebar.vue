<template>
  <div class="sidebar-container">
    <!-- Top Button Group -->
    <div class="button-group top-buttons">
      <button 
        class="upload-btn"
        @click="handleUpload"
        :disabled="isLoading"
      >
        <span class="upload-btn-text">Upload</span>
      </button>
      
      <button 
        class="sidebar-btn"
        @click="handleCutter"
        :disabled="isLoading"
      >
        <span class="btn-text">Cutter</span>
      </button>
      
      <button 
        class="sidebar-btn"
        @click="handleMaterial"
        :disabled="isLoading"
      >
        <span class="btn-text">Material</span>
      </button>
    </div>

    <!-- Spacer to push bottom buttons down -->
    <div class="spacer"></div>

    <!-- Bottom Button Group -->
    <div class="button-group bottom-buttons">
      <button 
        class="sidebar-btn remove-doubles-btn"
        @click="handleRemoveDoubles"
        :disabled="isLoading"
      >
        <span class="btn-text">Remove Doubles</span>
      </button>
      
      <button 
        class="sidebar-btn"
        @click="handleFixColors"
        :disabled="isLoading"
      >
        <span class="btn-text">Fix Colors</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import eventBus from '../eventBus'

// State
const isLoading = ref(false)

// Event handlers
const handleUpload = async () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.svg,.dxf,.ai,.pdf'
  input.onchange = async (event) => {
    const file = event.target.files[0]
    if (file) {
      await uploadFile(file)
    }
  }
  input.click()
}

const handleCutter = () => {
  console.log('Cutter button clicked')
}

const handleMaterial = () => {
  console.log('Material button clicked')
}

const handleRemoveDoubles = async () => {
  console.log('Remove Doubles button clicked')
}

const handleFixColors = async () => {
  console.log('Fix Colors button clicked')
  isLoading.value = true
}

// File upload handler
const uploadFile = async (file) => {
  isLoading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await fetch('/api/pdf_extraction', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error('Upload failed')
    }
    
    const result = await response.json()
    console.log('Upload successful:')
    const lines = result.lines
    // console.log('Extracted lines:', lines)
    // alert('File uploaded successfully!')

    eventBus.emit('lines-updated', lines)
    
    // Emit event to refresh the view
    window.dispatchEvent(new CustomEvent('file-uploaded', { detail: result }))
    
  } catch (error) {
    console.error('Upload error:', error)
    alert('Error uploading file: ' + error.message)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.sidebar-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20px 0;
  background: #ffffff;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0 15px;
}

.top-buttons {
  margin-bottom: 0;
}

.bottom-buttons {
  margin-bottom: 20px;
}

.spacer {
  flex: 1;
}

.sidebar-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid #353535;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.sidebar-btn:active:not(:disabled) {
  transform: translateX(2px);
}

.btn-text {
  flex: 1;
  text-align: left;
  color: #353535;
}

.upload-btn-text {
  color: #FFFFFF;
}

.upload-btn {
  justify-content: center;
  padding: 14px 16px;
  background: #EF8C19;
  margin: 10px 0px;
  border: 0px transparent;
  border-radius: 8px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}
</style>