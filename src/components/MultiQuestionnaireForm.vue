<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'
import ReviewPage from './ReviewPage.vue'

const route = useRoute()

const questions = [
  {
    type: 'short-answer',
    question: 'What is your name?'
  },
  {
    type: 'short-answer',
    question: 'How old are you?'
  },
  {
    type: 'multiple-choice',
    question: 'What is your gender?',
    options: ['Male', 'Female']
  },
  {
    type: 'short-answer',
    question: 'What is your height (cm)?'
  },
  {
    type: 'short-answer',
    question: 'What is your weight (kg)?'
  },
  {
    type: 'multiple-choice',
    question: 'Do you have prior experience with squat training?',
    options: ['Yes', 'No']
  },
  {
    type: 'multiple-choice',
    question: 'How often do you perform squat exercises per week?',
    options: ['Never', '1-2 times', '3-4 times', '5 or more times']
  },
  {
    type: 'multiple-choice',
    question: 'How many squat repetitions do you usually perform in one training session?',
    options: ['Less than 10', '10-20', '21-30', 'More than 30']
  },
  {
    type: 'multiple-choice',
    question: 'Do you have a fixed training routine or schedule?',
    options: ['Yes', 'No']
  },
  {
    type: 'multiple-choice',
    question: 'For how long have you been consistently practicing squat exercises?',
    options: ['I have never practiced consistently', 'Less than 3 months', '3-6 months', 'More than 6 months']
  },
  {
    type: 'scale',
    question: 'How difficult is it for you to exercise consistently?',
    min: 1,
    max: 7,
    minLabel: 'Very easy',
    maxLabel: 'Very difficult'
  },
  {
    type: 'checkbox',
    question: 'What other purposes do you have for squatting, besides preventing muscle weakening in old age?',
    options: ['Improve overall health', 'Increase leg muscle strength', 'Improve balance and mobility', 'Other'],
    hasOther: true
  },
  {
    type: 'checkbox',
    question: 'What usually motivates you to keep training?',
    options: ['Seeing physical progress', 'Receiving support from others', 'Feeling healthier and more energetic', 'Achieving set goals']
  },
  {
    type: 'scale',
    question: 'How much do you rely on external motivation from a coach or system?',
    min: 1,
    max: 7,
    minLabel: 'Not at all',
    maxLabel: 'Very much'
  },
  {
    type: 'multiple-choice',
    question: 'What type of motivation is most effective for you?',
    options: ['Encouraging and inspiring messages', 'Progress statistics and data', 'Challenges or competitions', 'Other'],
    hasOther: true
  },
  {
    type: 'multiple-choice',
    question: 'In the next 6 months, do you intend to increase your squat training frequency or intensity?',
    options: ['Yes, I plan to increase', 'No, I do not plan to change', 'Unsure']
  },
  {
    type: 'multiple-choice',
    question: 'What is your biggest challenge in maintaining squat training consistency?',
    options: ['Lack of time', 'Lack of motivation', 'Uncertainty about proper technique', 'Injury or discomfort during training', 'Other'],
    hasOther: true
  },
  {
    type: 'multiple-choice',
    question: 'How do you usually overcome these challenges?',
    options: ['Adjusting my training schedule', 'Seeking encouragement from a coach or friends', 'Reducing training intensity', 'I have never tried', 'Other'],
    hasOther: true
  },
  {
    type: 'scale',
    question: 'Do you feel that the benefits of squat training outweigh the challenges?',
    min: 1,
    max: 7,
    minLabel: 'Not at all',
    maxLabel: 'Very much'
  },
  {
    type: 'multiple-choice',
    question: 'Do you have any injury history or health conditions that should be considered during squat exercises?',
    options: ['Yes', 'No'],
    hasOther: true
  },
  {
    type: 'multiple-choice',
    question: 'Do you experience pain or discomfort while performing squats?',
    options: ['Yes, Please specify', 'No'],
    hasOther: true
  },
  {
    type: 'scale',
    question: 'How important is it for you to receive safety recommendations during training?',
    min: 1,
    max: 7,
    minLabel: 'Not important',
    maxLabel: 'Very important'
  },
  {
    type: 'scale',
    question: 'How satisfied are you with your squat training progress so far?',
    min: 1,
    max: 7,
    minLabel: 'Very dissatisfied',
    maxLabel: 'Very satisfied'
  },
  {
    type: 'multiple-choice',
    question: 'Would you like to increase your squat repetitions in the next training session?',
    options: ['Yes', 'No']
  },
  {
    type: 'multiple-choice',
    question: 'How many additional repetitions do you think would be realistic for your next session?',
    options: ['1-5 reps', '6-10 reps', 'More than 10 reps']
  }
];


const currentStep = ref(0)
const isReviewing = ref(false)
const isLoading = ref(false)
const formData = ref<Record<string, {
  value: string | number
  values?: string[]
  otherValue?: string
}>>(
  questions.reduce((acc, question, index) => {
    const key = `q${index}`
    acc[key] = {
      value: question.type === 'scale' ? question.min : '',
      values: question.type === 'checkbox' ? [] : undefined,
      otherValue: ''
    }
    return acc
  }, {} as Record<string, any>)
)

const rules = computed(() => {
  const rulesObj: Record<string, any> = {}
  
  questions.forEach((q, index) => {
    const key = `q${index}`
    rulesObj[key] = { value: { required } }
    
    if (q.type === 'multiple-choice' && q.hasOther) {
      rulesObj[key].otherValue = { 
        requiredIfOther: (value: string) => ({
          $validator: () => formData.value[key]?.value !== 'Other' || !!value?.trim() || formData.value[key]?.value !== 'Yes, Please specify',
          $message: 'Please specify your choice'
        })
      }
    }
    
    if (q.type === 'checkbox') {
      rulesObj[key].values = { required, minLength: minLength(1) }
      if (q.hasOther) {
        rulesObj[key].otherValue = {
          requiredIfOther: (value: string) => ({
            $validator: () => !formData.value[key]?.values?.includes('Other') || !!value?.trim(),
            $message: 'Please specify your other choices'
          })
        }
      }
    }
    
    if (q.type === 'short-answer') {
      rulesObj[key].value = { required, minLength: minLength(1) }
    }
  })
  
  return rulesObj
})

const v$ = useVuelidate(rules, formData)

const progress = computed(() => {
  return ((currentStep.value + 1) / questions.length) * 100
})

const nextStep = async () => {
  isLoading.value = true
  
  const currentQuestion = questions[currentStep.value]
  const key = `q${currentStep.value}`
  
  // Initialize answer object if not exists
  if (!formData.value[key]) {
    formData.value[key] = {
      value: '',
      values: [],
      otherValue: ''
    }
  }

  // Validate current step
  let isValid = true
  
  // Ada kemungkinan bagian ini masih butuh revisi
  await v$.value[key].$validate()
  if (questions[currentStep.value].type !== 'checkbox') {
    isValid = !v$.value[key].$error
  }
   
  // Additional validation for checkbox questions
  if (questions[currentStep.value].type === 'checkbox') {
    if (formData.value[key]?.values?.includes('Other')) {
      await v$.value[key].otherValue.$validate()
      isValid = isValid && !v$.value[key].otherValue.$error
    }
  }

  if (!isValid) {
    const currentQuestion = questions[currentStep.value]
    let errorMessage = ''

    if (currentQuestion.type === 'short-answer') {
      errorMessage = 'Please provide an answer to this question'
    } else if (currentQuestion.type === 'multiple-choice') {
      errorMessage = 'Please select one of the options'
    } else if (currentQuestion.type === 'checkbox') {
      errorMessage = 'Please select at least one option'
    } else if (currentQuestion.type === 'scale') {
      errorMessage = 'Please select a value on the scale'
    }

    alert(errorMessage)
    isLoading.value = false
    return
  }

  if (isValid) {
    if (currentStep.value < questions.length - 1) {
      currentStep.value++
    } else {
      isReviewing.value = true
    }
  }
  
  isLoading.value = false
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
    
    // Get exerciseId from route params
    const exerciseId = route.params.exerciseId
    
    // Submit to API
    const response = await fetch(`/api/submit-questionnaire?exerciseId=${exerciseId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"personalization" : result})
    })
    
    if (!response.ok) {
      throw new Error('Failed to submit questionnaire')
    }
    
    // Navigate to feedback page
    window.location.href = `/feedback/${exerciseId}?type=performance_personalization`
  } finally {
    isLoading.value = false
  }
}

const getAnswer = (type: string, index: number) => {
  const answer = formData.value[`q${index}`]
  if (!answer) return ''

  switch (type) {
    case 'multiple-choice':
      return answer.value === 'Other' || answer.value === 'Yes, Please specify' ? answer.otherValue : answer.value
    case 'checkbox':
      const answers = [...answer.values]
      if (answers.includes('Other')) {
        answers.splice(answers.indexOf('Other'), 1)
        answers.push(answer.otherValue)
      }
      return answers
    case 'scale':
      const question = questions[index]
      return `${answer.value}/${question.max} (${question.minLabel}=${question.min}, ${question.maxLabel}=${question.max})`
    case 'short-answer':
      return answer.value
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
                  'selected': formData[`q${currentStep}`]?.value === option 
                }]"
                @click="formData[`q${currentStep}`].value = option"
              >
                <div class="radio-indicator"></div>
                <span>{{ option }}</span>
              </div>
            </div>
            <div v-if="formData[`q${currentStep}`]?.value === 'Other' || formData[`q${currentStep}`]?.value === 'Yes, Please specify'" class="mt-3">
              <input
                type="text"
                v-model="formData[`q${currentStep}`].otherValue"
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
                  'selected': formData[`q${currentStep}`]?.values?.includes(option) 
                }]"
                @click="
                  formData[`q${currentStep}`].values?.includes(option)
                    ? formData[`q${currentStep}`].values = formData[`q${currentStep}`].values.filter(x => x !== option)
                    : formData[`q${currentStep}`].values.push(option);
                  console.log('Checkbox selection:', {
                    question: questions[currentStep].question,
                    selectedValues: formData[`q${currentStep}`].values,
                    hasOther: questions[currentStep].hasOther,
                    otherValue: formData[`q${currentStep}`].otherValue
                  })
                "
              >
                <div class="checkbox-indicator"></div>
                <span>{{ option }}</span>
              </div>
            </div>
            <div v-if="formData[`q${currentStep}`]?.values?.includes('Other')" class="mt-3">
              <input
                type="text"
                v-model="formData[`q${currentStep}`].otherValue"
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
                  v-for="n in questions[currentStep].max"
                  :key="n"
                  :class="['scale-button', { 'selected': formData[`q${currentStep}`]?.value === n }]"
                  @click="formData[`q${currentStep}`].value = n"
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
              v-model="formData[`q${currentStep}`].value"
              class="form-control custom-textarea"
              rows="4"
              placeholder="Enter your answer here..."
            ></textarea>
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