<script setup lang="ts">
import FileUpload from '../components/FileUpload.vue'
import { ref } from 'vue'

const analysisResult = ref(null)

const handleFileUploaded = (result: any) => {
  analysisResult.value = result
}
</script>

<template>
  <div class="results-page">
    <div class="results-container">
      <h2>Upload Your Results</h2>
      <FileUpload @file-uploaded="handleFileUploaded" />
      
      <div v-if="analysisResult" class="analysis-results">
        <h3>Analysis Results</h3>
        <pre>{{ JSON.stringify(analysisResult, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.results-page {
  min-height: 100vh;
  background-color: #FCE7C8;
  padding: 2rem;
  
  .results-container {
    max-width: 800px;
    margin: 0 auto;
    background-color: #fff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    
    h2 {
      color: #333;
      margin-bottom: 2rem;
    }
    
    .analysis-results {
      margin-top: 2rem;
      padding: 1rem;
      background-color: #f8f9fa;
      border-radius: 4px;
      
      pre {
        margin: 0;
        white-space: pre-wrap;
      }
    }
  }
}
</style>