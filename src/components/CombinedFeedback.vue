<template>
  <div class="container combined-feedback">
    <div v-if="isLoadingAnalysis" class="loading-overlay">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-if="analysisError" class="error-message alert alert-danger">
      {{ analysisError }}
    </div>

    <div v-if="feedbackData" class="feedback-results">
      <h3 class="results-title mb-4">Exercise Analysis</h3>
      
      <div v-for="(item, index) in feedbackData" :key="index" class="repetition-group">
        <div class="repetition-header" :class="headerClass(item.state)">
          <h4>Repetition {{ item.repetition }}</h4>
          <span class="status-badge">{{ item.state }}</span>
        </div>

        <div class="feedback-details">
          <div v-for="(feedback, fIndex) in item.feedbacks" :key="fIndex" class="feedback-item">
            <div class="comparison-row">
              <div class="image-section">
                <h5>Your Form</h5>
                <img
                  v-show="feedback.feedback !== -1"
                  :src="`data:image/jpg;base64, ${feedback.img_64}`"
                  class="form-image"
                  alt="Exercise snapshot"
                >
                <div class="feedback-message alert" :class="[messageClass(item.state), { 'text-center': feedback.feedback === -1 }]">
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

      <hr class="section-divider">

      <!-- Feedback cards grid -->
      <div
        class="cards-grid"
        ref="feedbackGrid"
        :class="{ 'collapsed': gridCollapsed }"
      >
        <div v-if="isLoadingMotivation" class="loading-overlay">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <div v-if="motivationError" class="error-message alert alert-danger">
          {{ motivationError }}
        </div>
        <template v-if="$route.query.type === 'performance_personalization'">
          <div class="feedback-section">
            <h3 class="section-title">Message based on Performance Data</h3>
            <div class="cards-grid">
              <div class="feedback-card" style="background: #B5D8F7">
                <h4 class="card-title">Feedback</h4>
                <p class="card-text">{{ performanceFeedbackData?.performance_feedback }}</p>
              </div>
              
              <div class="feedback-card" style="background: #FFD9B3">
                <h4 class="card-title">Motivation</h4>
                <p class="card-text">{{ performanceFeedbackData?.motivation }}</p>
              </div>
              
              <div class="feedback-card" style="background: #FFB3B3">
                <h4 class="card-title">Safety Notes ❗</h4>
                <p class="card-text">{{ performanceFeedbackData?.safety }}</p>
              </div>
              
              <div class="feedback-card" style="background: #B3D9B3">
                <h4 class="card-title">Suggestion</h4>
                <p class="card-text">{{ performanceFeedbackData?.suggestion }}</p>
              </div>
            </div>
          </div>

          <hr class="section-divider">

          <div class="feedback-section">
            <h3 class="section-title">Message based on Performance Data and Personalization Data</h3>
            <div class="cards-grid">
              <div class="feedback-card" style="background: #B5D8F7">
                <h4 class="card-title">Feedback</h4>
                <p class="card-text">{{ motivationData?.performance_feedback }}</p>
              </div>
              
              <div class="feedback-card" style="background: #FFD9B3">
                <h4 class="card-title">Motivation</h4>
                <p class="card-text">{{ motivationData?.motivation }}</p>
              </div>
              
              <div class="feedback-card" style="background: #FFB3B3">
                <h4 class="card-title">Safety Notes ❗</h4>
                <p class="card-text">{{ motivationData?.safety }}</p>
              </div>
              
              <div class="feedback-card" style="background: #B3D9B3">
                <h4 class="card-title">Suggestion</h4>
                <p class="card-text">{{ motivationData?.suggestion }}</p>
              </div>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="cards-grid">
            <div class="feedback-card" style="background: #B5D8F7">
              <h4 class="card-title">Feedback</h4>
              <p class="card-text">{{ motivationData?.performance_feedback }}</p>
            </div>
            
            <div class="feedback-card" style="background: #FFD9B3">
              <h4 class="card-title">Motivation</h4>
              <p class="card-text">{{ motivationData?.motivation }}</p>
            </div>
            
            <div class="feedback-card" style="background: #FFB3B3">
              <h4 class="card-title">Safety Notes ❗</h4>
              <p class="card-text">{{ motivationData?.safety }}</p>
            </div>
            
            <div class="feedback-card" style="background: #B3D9B3">
              <h4 class="card-title">Suggestion</h4>
              <p class="card-text">{{ motivationData?.suggestion }}</p>
            </div>
          </div>
        </template>
      </div>
      
      <hr class="section-divider">
      
      <!-- Feedback Questionnaire CTA -->
      <div class="questionnaire-cta">
        <div class="cta-buttons">
          <button
            class="cta-button secondary"
            @click="showInstructionsModal = true"
            aria-label="Show instructions"
          >
            Show Instructions
          </button>
          <button
            class="cta-button primary"
            @click="showModal = true"
            aria-label="Provide additional feedback"
            :disabled="!motivationData || isLoadingMotivation"
          >
            Give Me Your Evaluation
          </button>
          <div v-if="$route.query.type === 'performance_personalization'" class="personalization-note alert alert-info">
            This evaluation is different from the previous one because the four messages here have been added with personalized data specifically for you.
          </div>
        </div>
      </div>
    </div>

    <FeedbackModal
      v-model:show="showModal"
      @submit-success="submissionComplete = true"
    />

    <FeedbackInstructionsModal
      :show="showInstructionsModal"
      @close="showInstructionsModal = false"
    />

    <Transition name="toast">
      <div
        v-if="submissionComplete"
        class="success-toast"
        role="alert"
        aria-live="polite"
      >
        <i class="fas fa-check-circle"></i>
        Thank you for your feedback!
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import FeedbackModal from './FeedbackModal.vue'
import FeedbackInstructionsModal from './FeedbackInstructionsModal.vue'

const route = useRoute()
const exerciseId = typeof route.params.exerciseId === 'string' ? route.params.exerciseId : route.params.exerciseId[0]
const feedbackType = typeof route.query.type === 'string' ? route.query.type : ''

console.log('Feedback slug:', exerciseId)
console.log('Feedback type:', feedbackType)

const showModal = ref(false)
const showInstructionsModal = ref(false)
const submissionComplete = ref(false)
const instructionsSeen = ref(false)

onMounted(() => {
  if (!instructionsSeen.value) {
    showInstructionsModal.value = true
    instructionsSeen.value = true
  }
})
</script>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'CombinedFeedback',
  watch: {
    feedbackData(newVal) {
      if (newVal && newVal.length > 0) {
        const exerciseId = typeof this.$route.params.exerciseId === 'string'
          ? this.$route.params.exerciseId
          : this.$route.params.exerciseId[0];
        const type = typeof this.$route.query.type === 'string'
          ? this.$route.query.type
          : '';
        this.fetchMotivation(exerciseId, type);
      }
    }
  },
  data() {
    return {
      selectedFile: null as File|null,
      feedbackData: null as any,
      motivationData: null as any,
      performanceFeedbackData: null as any,
      isLoadingAnalysis: false,
      isLoadingMotivation: false,
      analysisError: null as string|null,
      motivationError: null as string|null,
      gridCollapsed: false,
      gridOriginalState: null as string|null,
      $refs: {
        feedbackGrid: null as HTMLElement|null
      }
    };
  },
  mounted() {
    this.fetchAnalysis();
  },
  methods: {
    async fetchAnalysis() {
      this.isLoadingAnalysis = true;
      this.analysisError = null;
      
      const exerciseId = this.$route.params.exerciseId;
      if (!exerciseId) {
        this.analysisError = 'Exercise ID is required';
        this.isLoadingAnalysis = false;
        return;
      }

      try {
        const response = await fetch(`/api/analyze?exerciseId=${exerciseId}`, {
          method: 'GET'
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        this.feedbackData = await response.json();
      } catch (error) {
        this.analysisError = error instanceof Error ? error.message : 'Failed to fetch analysis';
        console.error('Analysis failed:', error);
      } finally {
        this.isLoadingAnalysis = false;
      }
    },
    handleFileChange(event: Event) {
      const input = event.target as HTMLInputElement;
      this.selectedFile = input.files?.[0] || null;
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
    },
    async fetchMotivation(exerciseId: string, type: string) {
      this.isLoadingMotivation = true;
      this.motivationError = null;
      
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000);
      
      try {
        if (type === 'performance_personalization') {
          // Fetch performance feedback first
          const perfResponse = await fetch(`/api/llm-feedback?exerciseId=${exerciseId}&type=performance`, {
            method: 'GET',
            signal: controller.signal
          });
          
          if (!perfResponse.ok) {
            throw new Error(`HTTP error! status: ${perfResponse.status}`);
          }
          this.performanceFeedbackData = await perfResponse.json();

          // Then fetch personalized feedback
          const personalResponse = await fetch(`/api/llm-feedback?exerciseId=${exerciseId}&type=${type}`, {
            method: 'GET',
            signal: controller.signal
          });
          
          if (!personalResponse.ok) {
            throw new Error(`HTTP error! status: ${personalResponse.status}`);
          }
          this.motivationData = await personalResponse.json();
        } else {
          // Original behavior for other types
          const response = await fetch(`/api/llm-feedback?exerciseId=${exerciseId}&type=${type}`, {
            method: 'GET',
            signal: controller.signal
          });
          
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          this.motivationData = await response.json();
        }
      } catch (error) {
        this.motivationError = error instanceof Error ? error.message : 'Failed to fetch motivation';
        this.triggerGridCollapse();
      } finally {
        clearTimeout(timeoutId);
        this.isLoadingMotivation = false;
      }
    },
    triggerGridCollapse() {
      // Store current grid state
      this.gridOriginalState = this.$refs.feedbackGrid?.innerHTML ?? null;
      this.gridCollapsed = true;
      
      // Rehydrate after animation if needed
      setTimeout(() => {
        if (this.gridCollapsed && this.gridOriginalState) {
          this.gridCollapsed = false;
        }
      }, 3000);
    }
  }
});
</script>

<style lang="scss" scoped>
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
  
  &.text-center {
    text-align: center;
  }
}

.instruction-text {
  background: white;
  padding: 1rem;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  z-index: 10;
}

.cards-grid {
  position: relative;
  transition: all 0.3s ease;
}

.cards-grid.collapsed {
  max-height: 0;
  overflow: hidden;
  opacity: 0;
  margin: 0;
  padding: 0;
}

.error-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  text-align: center;
  z-index: 10;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}


@media (max-width: 768px) {
  .comparison-row {
    grid-template-columns: 1fr;
  }
}

.cards-grid {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 16px;
}

.feedback-section .cards-grid {
  grid-template-columns: repeat(2, 1fr);
}

@media (max-width: 768px) {
  .feedback-section .cards-grid,
  .cards-grid {
    grid-template-columns: 1fr;
  }
}

.feedback-card {
  padding: 16px;
  border-radius: 8px;
  transition: filter 0.2s ease;
}

.feedback-card:hover {
  filter: brightness(110%);
}

.card-title {
  font-family: sans-serif;
  font-size: 16pt;
  font-weight: bold;
  margin-bottom: 12px;
}

.card-text {
  font-family: sans-serif;
  font-size: 12pt;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
}

.section-divider {
  border: 0;
  height: 2px;
  background: #000000;
  margin: 2rem 0;
  width: 100%;
}

.feedback-section {
  margin-bottom: 2rem;
}

.section-title {
  font-family: sans-serif;
  font-size: 18pt;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
}

.questionnaire-cta {
  text-align: center;
  margin: 3rem 0;
  
  .cta-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .cta-button {
    padding: 1rem 2rem;
    border: none;
    border-radius: 2rem;
    font-size: 1.25rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    
    &.primary {
      background-color: #F0A04B;
      color: white;
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        background-color: #e0903b;
      }
    }
    
    &.secondary {
      background-color: #B1C29E;
      color: white;
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        background-color: #9aae85;
      }
    }
    
    &:active {
      transform: translateY(0);
    }

    &:disabled {
      background-color: #cccccc;
      cursor: not-allowed;
      opacity: 0.7;
      box-shadow: none;
      transform: none;
    }
  }
}

.success-toast {
  position: fixed;
  bottom: 2rem;
  background: #B1C29E;
  color: white;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>