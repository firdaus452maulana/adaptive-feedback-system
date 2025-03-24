<template>
  <div class="container combined-feedback">
    <div class="upload-section card p-4 mb-5">
      <h2 class="mb-4">Upload Exercise Video</h2>
      <form @submit.prevent="handleSubmit" class="upload-form">
        <div class="custom-file mb-3">
          <input 
            type="file" 
            class="custom-file-input"
            id="exerciseVideo"
            accept=".json,.txt"
            @change="handleFileChange"
          >
          <label class="custom-file-label" for="exerciseVideo">
            {{ selectedFile ? selectedFile.name : 'Choose file...' }}
          </label>
        </div>
        <button type="submit" class="btn btn-primary btn-lg">
          Analyze Movement
        </button>
      </form>
    </div>

    <div v-if="feedbackData" class="feedback-results">
      <h3 class="results-title mb-4">Exercise Analysis</h3>
      
      <div v-for="(item, index) in feedbackData" :key="index" class="repetition-group">
        <div class="repetition-header" :class="headerClass(item.state)">
          <h4>Repetition {{ item.repetition + 1 }}</h4>
          <span class="status-badge">{{ item.state }}</span>
        </div>

        <div class="feedback-details">
          <div v-for="(feedback, fIndex) in item.feedbacks" :key="fIndex" class="feedback-item">
            <div class="comparison-row">
              <div class="image-section">
                <h5>Your Form</h5>
                <img 
                  :src="`data:image/jpg;base64, ${feedback.img_64}`" 
                  class="form-image"
                  alt="Exercise snapshot"
                >
                <div class="feedback-message alert" :class="messageClass(item.state)">
                  {{ feedback.feedback_desc }}
                </div>
              </div>
              
              <div class="feedback-section">
                <div class="correct-form">
                  <h5>Recommended Form</h5>
                  <img
                    :src="`${feedback.feedback_form}`"
                    class="correct-image"
                    alt="Correct form example"
                  >
                  <p class="instruction-text">
                    {{ feedback.feedback_recommendation }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'CombinedFeedback',
  data() {
    return {
      selectedFile: null as File|null,
      feedbackData: null as any,
    };
  },
  methods: {
    handleFileChange(event: Event) {
      const input = event.target as HTMLInputElement;
      this.selectedFile = input.files?.[0] || null;
    },
    async handleSubmit() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append('file', this.selectedFile);

      try {
        const response = await fetch('/api/', {
          method: 'POST',
          body: formData
        });
        this.feedbackData = await response.json();
      } catch (error) {
        console.error('Analysis failed:', error);
      }
    },
    headerClass(state: string) {
      return {
        'header-success': state === 'CORRECT',
        'header-warning': state === 'IMPROPER',
        'header-error': state === 'FAILED'
      };
    },
    messageClass(state: string) {
      return {
        'alert-success': state === 'CORRECT',
        'alert-warning': state === 'IMPROPER',
        'alert-danger': state === 'FAILED'
      };
    }
  }
});
</script>

<style scoped>
.combined-feedback {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.upload-section {
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.custom-file-input {
  opacity: 0;
  position: absolute;
  z-index: -1;
}

.custom-file-label {
  display: block;
  padding: 0.75rem 1rem;
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.custom-file-label:hover {
  border-color: #007bff;
}

.btn-lg {
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
}

.feedback-results {
  margin-top: 2rem;
}

.repetition-header {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-success {
  background: #d4edda;
  color: #155724;
}

.header-warning {
  background: #fff3cd;
  color: #856404;
}

.header-error {
  background: #f8d7da;
  color: #721c24;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: bold;
}

.comparison-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.form-image, .correct-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feedback-message {
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.instruction-text {
  background: white;
  padding: 1rem;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

@media (max-width: 768px) {
  .comparison-row {
    grid-template-columns: 1fr;
  }
}
</style>