<script setup lang="ts">
import { ref, computed } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'
import ReviewPage from './ReviewPage.vue'

const currentStep = ref(0)
const isReviewing = ref(false)
const isLoading = ref(false)
const formData = ref({
  multipleChoice: '',
  multipleChoiceOther: '',
  checkboxes: [] as string[],
  checkboxOther: '',
  scale: 4,
  shortAnswer: ''
})

const rules = {
  multipleChoice: { required },
  shortAnswer: { required, minLength: minLength(3) }
}

const v$ = useVuelidate(rules, formData)

const questions = [
  {
    type: 'multiple-choice',
    question: 'How often do you exercise?',
    options: ['Daily', 'Weekly', '2-3 times per week', 'Monthly', 'Other'],
    hasOther: true
  },
  {
    type: 'checkbox',
    question: 'What types of exercise do you prefer?',
    options: ['Running', 'Swimming', 'Cycling', 'Weight Training', 'Other'],
    hasOther: true
  },
  {
    type: 'scale',
    question: 'How would you rate your current fitness level?',
    min: 1,
    max: 7,
    minLabel: 'Beginner',
    maxLabel: 'Advanced'
  },
  {
    type: 'short-answer',
    question: 'What are your fitness goals?'
  }
]

const progress = computed(() => {
  return ((currentStep.value + 1) / questions.length) * 100
})

const nextStep = async () => {
  isLoading.value = true
  const result = await v$.value.$validate()
  
  setTimeout(() => {
    if (result) {
      if (currentStep.value < questions.length - 1) {
        currentStep.value++
      } else {
        isReviewing.value = true
      }
    }
    isLoading.value = false
  }, 300)
}

const prevStep = () => {
  if (isReviewing.value) {
    isReviewing.value = false
  } else if (currentStep.value > 0) {
    currentStep.value--
  }
}

const jumpToQuestion = (index: number) => {
  isReviewing.value = false
  currentStep.value = index
}

const generateJSON = async () => {
  isLoading.value = true
  
  try {
    const result = questions.map((q, index) => ({
      question: q.question,
      answer: getAnswer(q.type, index)
    }))
    
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'questionnaire-results.json'
    a.click()
    URL.revokeObjectURL(url)
  } finally {
    isLoading.value = false
  }
}

const getAnswer = (type: string, index: number) => {
  switch (type) {
    case 'multiple-choice':
      return formData.value.multipleChoice === 'Other' 
        ? formData.value.multipleChoiceOther 
        : formData.value.multipleChoice
    case 'checkbox':
      return formData.value.checkboxes.includes('Other')
        ? [...formData.value.checkboxes.filter(x => x !== 'Other'), formData.value.checkboxOther]
        : formData.value.checkboxes
    case 'scale':
      return formData.value.scale
    case 'short-answer':
      return formData.value.shortAnswer
    default:
      return ''
  }
}
</script>

<template>
  <div class="questionnaire-form">
    <div class="progress-container">
      <div class="progress">
        <div 
          class="progress-bar" 
          role="progressbar" 
          :style="{ width: `${progress}%` }" 
          :aria-valuenow="progress" 
          aria-valuemin="0" 
          aria-valuemax="100"
        >
          {{ Math.round(progress) }}%
        </div>
      </div>
      <div class="steps-indicator">
        <div 
          v-for="(_, index) in questions" 
          :key="index"
          :class="['step', { 
            'active': index === currentStep,
            'completed': index < currentStep
          }]"
          @click="jumpToQuestion(index)"
        >
          {{ index + 1 }}
        </div>
      </div>
    </div>

    <div v-if="!isReviewing" class="question-container">
      <transition name="fade" mode="out-in">
        <div :key="currentStep">
          <div v-if="questions[currentStep].type === 'multiple-choice'" class="mb-4">
            <h3>{{ questions[currentStep].question }}</h3>
            <div class="options-grid">
              <div 
                v-for="option in questions[currentStep].options" 
                :key="option"
                :class="['option-card', { 
                  'selected': formData.multipleChoice === option 
                }]"
                @click="formData.multipleChoice = option"
              >
                <div class="radio-indicator"></div>
                <span>{{ option }}</span>
              </div>
            </div>
            <div v-if="formData.multipleChoice === 'Other'" class="mt-3">
              <input
                type="text"
                v-model="formData.multipleChoiceOther"
                class="form-control custom-input"
                placeholder="Please specify"
              >
            </div>
          </div>

          <div v-if="questions[currentStep].type === 'checkbox'" class="mb-4">
            <h3>{{ questions[currentStep].question }}</h3>
            <div class="options-grid">
              <div 
                v-for="option in questions[currentStep].options" 
                :key="option"
                :class="['option-card', { 
                  'selected': formData.checkboxes.includes(option) 
                }]"
                @click="
                  formData.checkboxes.includes(option)
                    ? formData.checkboxes = formData.checkboxes.filter(x => x !== option)
                    : formData.checkboxes.push(option)
                "
              >
                <div class="checkbox-indicator"></div>
                <span>{{ option }}</span>
              </div>
            </div>
            <div v-if="formData.checkboxes.includes('Other')" class="mt-3">
              <input
                type="text"
                v-model="formData.checkboxOther"
                class="form-control custom-input"
                placeholder="Please specify"
              >
            </div>
          </div>

          <div v-if="questions[currentStep].type === 'scale'" class="mb-4">
            <h3>{{ questions[currentStep].question }}</h3>
            <div class="scale-container">
              <span class="scale-label">{{ questions[currentStep].minLabel }}</span>
              <div class="scale-buttons">
                <button
                  v-for="n in 7"
                  :key="n"
                  :class="['scale-button', { 'selected': formData.scale === n }]"
                  @click="formData.scale = n"
                >
                  {{ n }}
                </button>
              </div>
              <span class="scale-label">{{ questions[currentStep].maxLabel }}</span>
            </div>
          </div>

          <div v-if="questions[currentStep].type === 'short-answer'" class="mb-4">
            <h3>{{ questions[currentStep].question }}</h3>
            <textarea
              v-model="formData.shortAnswer"
              class="form-control custom-textarea"
              rows="4"
              placeholder="Enter your answer here..."
            ></textarea>
            <div v-if="v$.shortAnswer.$error" class="error-message">
              Please enter at least 3 characters
            </div>
          </div>
        </div>
      </transition>
    </div>

    <ReviewPage
      v-else
      :questions="questions"
      :answers="formData"
      @edit-question="jumpToQuestion"
    />

    <div class="button-container">
      <button 
        @click="prevStep" 
        class="btn btn-outline-secondary" 
        :disabled="currentStep === 0 && !isReviewing"
      >
        <span class="button-content">
          <i class="fas fa-arrow-left"></i>
          Previous
        </span>
      </button>
      
      <button 
        v-if="!isReviewing"
        @click="nextStep" 
        class="btn btn-primary"
        :disabled="isLoading"
      >
        <span class="button-content">
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
          <span v-else>
            {{ currentStep === questions.length - 1 ? 'Review Answers' : 'Next' }}
            <i class="fas fa-arrow-right"></i>
          </span>
        </span>
      </button>
      
      <button 
        v-else
        @click="generateJSON" 
        class="btn btn-success"
        :disabled="isLoading"
      >
        <span class="button-content">
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
          <span v-else>
            Submit Quiz
            <i class="fas fa-check"></i>
          </span>
        </span>
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "sass:color";
.questionnaire-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);

  @media (min-width: 768px) {
    padding: 2rem;
  }

  .progress-container {
    margin-bottom: 2rem;

    .progress {
      height: 8px;
      background-color: #FCE7C8;
      border-radius: 999px;
      overflow: hidden;
      
      .progress-bar {
        background-color: #F0A04B;
        transition: width 0.3s ease;
      }
    }

    .steps-indicator {
      display: flex;
      justify-content: space-between;
      margin-top: 1rem;
      padding: 0 10px;

      .step {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: #fff;
        border: 2px solid #B1C29E;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;

        &.active {
          background-color: #B1C29E;
          color: #fff;
          transform: scale(1.1);
        }

        &.completed {
          background-color: #F0A04B;
          border-color: #F0A04B;
          color: #fff;
        }

        &:hover {
          transform: scale(1.1);
        }
      }
    }
  }

  .question-container {
    background-color: #fff;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    min-height: 300px;

    @media (min-width: 768px) {
      padding: 2rem;
    }

    h3 {
      color: #333;
      margin-bottom: 1.5rem;
      font-size: 1.5rem;
      line-height: 1.4;
    }
  }

  .options-grid {
    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));

    .option-card {
      padding: 1rem;
      border: 2px solid #B1C29E;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      gap: 1rem;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      &.selected {
        background-color: #B1C29E;
        color: #fff;
        border-color: #B1C29E;

        .radio-indicator,
        .checkbox-indicator {
          border-color: #fff;
          &::after {
            opacity: 1;
          }
        }
      }

      .radio-indicator,
      .checkbox-indicator {
        width: 20px;
        height: 20px;
        border: 2px solid #B1C29E;
        border-radius: 50%;
        position: relative;

        &::after {
          content: '';
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 10px;
          height: 10px;
          background-color: #fff;
          border-radius: 50%;
          opacity: 0;
          transition: opacity 0.2s ease;
        }
      }

      .checkbox-indicator {
        border-radius: 4px;

        &::after {
          width: 12px;
          height: 12px;
          background-color: transparent;
          border-right: 2px solid #fff;
          border-bottom: 2px solid #fff;
          transform: translate(-50%, -50%) rotate(45deg);
        }
      }
    }
  }

  .scale-container {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0;
    flex-direction: column;

    @media (min-width: 768px) {
      flex-direction: row;
    }

    .scale-label {
      color: #666;
      font-size: 0.9rem;
      min-width: 80px;
      text-align: center;
    }

    .scale-buttons {
      display: flex;
      gap: 0.5rem;
      flex: 1;
      justify-content: space-between;
      
      .scale-button {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 2px solid #B1C29E;
        background-color: #fff;
        color: #333;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;

        &:hover {
          transform: scale(1.1);
        }

        &.selected {
          background-color: #B1C29E;
          color: #fff;
        }
      }
    }
  }

  .custom-input,
  .custom-textarea {
    border: 2px solid #B1C29E;
    border-radius: 8px;
    padding: 0.75rem;
    transition: all 0.3s ease;

    &:focus {
      border-color: #F0A04B;
      box-shadow: 0 0 0 3px rgba(240, 160, 75, 0.2);
    }
  }

  .error-message {
    color: #dc3545;
    font-size: 0.875rem;
    margin-top: 0.5rem;
  }

  .button-container {
    display: flex;
    justify-content: space-between;
    gap: 1rem;

    .btn {
      min-width: 120px;
      position: relative;
      
      .button-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
      }
      
      &.btn-primary {
        background-color: #B1C29E;
        border-color: #B1C29E;
        
        &:hover {
          background-color: color.adjust(#B1C29E, $lightness: -10%);
        }
      }
      
      &.btn-success {
        background-color: #F0A04B;
        border-color: #F0A04B;
        
        &:hover {
          background-color: darken(#F0A04B, 10%);
        }
      }

      &:disabled {
        opacity: 0.7;
        cursor: not-allowed;
      }
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>