<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, email, minLength } from '@vuelidate/validators'

const props = defineProps<{
  show: boolean
}>()

const emit = defineEmits(['update:show', 'submit-success'])

const formData = ref({
  rating: null as number | null,
  comment: '',
  email: ''
})

const rules = {
  rating: { required },
  comment: { required, minLength: minLength(10) },
  email: { email }
}

const v$ = useVuelidate(rules, formData)

const questions = [
  {
    type: 'rating',
    question: 'How would you rate your experience?',
    min: 1,
    max: 5
  },
  {
    type: 'comment',
    question: 'What could we improve?'
  }
]

const isValid = computed(() => {
  return !v$.value.$invalid
})

const handleClose = () => {
  emit('update:show', false)
}

const handleBackdropClick = (event: MouseEvent) => {
  if ((event.target as HTMLElement).classList.contains('modal-backdrop')) {
    handleClose()
  }
}

const submitForm = async () => {
  const isValid = await v$.value.$validate()
  if (isValid) {
    emit('submit-success')
    handleClose()
  }
}

watch(() => props.show, (newVal) => {
  if (newVal) {
    document.body.classList.add('modal-open')
    document.addEventListener('keydown', handleKeydown)
  } else {
    document.body.classList.remove('modal-open')
    document.removeEventListener('keydown', handleKeydown)
  }
})

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    handleClose()
  }
}
</script>

<template>
  <Transition name="modal">
    <div 
      v-if="show"
      class="modal-backdrop"
      @click="handleBackdropClick"
      @keydown.esc="handleClose"
      role="dialog"
      aria-modal="true"
    >
      <div class="modal-container">
        <div class="modal-header">
          <h2>Feedback Form</h2>
          <button 
            class="close-button"
            @click="handleClose"
            aria-label="Close feedback form"
          >
            &times;
          </button>
        </div>

        <div class="modal-content">
          <div 
            v-for="(question, index) in questions"
            :key="index"
            class="question-card"
          >
            <h3>{{ question.question }}</h3>
            
            <div v-if="question.type === 'rating'" class="rating-grid">
              <button
                v-for="n in 5"
                :key="n"
                :class="['rating-button', { 'selected': formData.rating === n }]"
                @click="formData.rating = n"
                :aria-label="`Rate ${n} out of 5`"
              >
                {{ n }}
              </button>
            </div>

            <textarea
              v-if="question.type === 'comment'"
              v-model="formData.comment"
              class="comment-input"
              rows="4"
              placeholder="Enter your feedback..."
              aria-label="Feedback comments"
            ></textarea>
            
            <div 
              v-if="v$.comment.$error && question.type === 'comment'"
              class="error-message"
            >
              Please provide at least 10 characters
            </div>
          </div>

          <div class="email-field">
            <input
              type="email"
              v-model="formData.email"
              placeholder="Optional: Enter email for follow-up"
              class="email-input"
              aria-label="Email for follow-up"
            >
            <div v-if="v$.email.$error" class="error-message">
              Please enter a valid email address
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button
            class="submit-button"
            @click="submitForm"
            :disabled="!isValid"
            aria-label="Submit feedback"
          >
            Submit Feedback
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style lang="scss" scoped>
@use "sass:color";

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);

  .modal-header {
    padding: 1.5rem;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;

    h2 {
      margin: 0;
      color: #333;
      font-size: 1.5rem;
    }

    .close-button {
      background: none;
      border: none;
      font-size: 2rem;
      cursor: pointer;
      color: #666;
      padding: 0 0.5rem;

      &:hover {
        color: #333;
      }
    }
  }

  .modal-content {
    padding: 1.5rem;
    overflow-y: auto;

    .question-card {
      background: #fff;
      padding: 1.5rem;
      border-radius: 8px;
      margin-bottom: 1.5rem;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

      h3 {
        margin-top: 0;
        margin-bottom: 1rem;
        color: #444;
        font-size: 1.2rem;
      }
    }

    .rating-grid {
      display: grid;
      gap: 1rem;
      grid-template-columns: repeat(5, 1fr);

      .rating-button {
        padding: 0.8rem;
        border: 2px solid #B1C29E;
        border-radius: 8px;
        background: white;
        color: #666;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;

        &.selected {
          background: #B1C29E;
          color: white;
          transform: scale(1.05);
        }

        &:hover {
          transform: scale(1.05);
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
      }
    }

    .comment-input {
      width: 100%;
      padding: 1rem;
      border: 2px solid #B1C29E;
      border-radius: 8px;
      resize: vertical;
      min-height: 100px;
    }

    .email-field {
      margin-top: 1.5rem;

      .email-input {
        width: 100%;
        padding: 0.8rem;
        border: 1px solid #ddd;
        border-radius: 6px;
      }
    }

    .error-message {
      color: #dc3545;
      font-size: 0.9rem;
      margin-top: 0.5rem;
    }
  }

  .modal-footer {
    padding: 1.5rem;
    border-top: 1px solid #eee;
    text-align: right;

    .submit-button {
      background-color: #F0A04B;
      color: white;
      padding: 0.8rem 2rem;
      border: none;
      border-radius: 2rem;
      cursor: pointer;
      transition: all 0.2s ease;

      &:disabled {
        background-color: #ccc;
        cursor: not-allowed;
      }

      &:not(:disabled):hover {
        background-color: #e0903b;
        transform: translateY(-1px);
      }
    }
  }
}

@media (max-width: 768px) {
  .modal-container {
    width: 95%;
    
    .rating-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
}
</style>