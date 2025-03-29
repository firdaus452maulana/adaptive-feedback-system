<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'

const props = defineProps<{
  show: boolean
}>()

const emit = defineEmits(['update:show', 'submit-success'])

const formData = ref({
  ratings: {} as Record<string, number | null>,
  comment: ''
})

const rules = {
  ratings: {
    $each: {
      required
    }
  }
}

const v$ = useVuelidate(rules, formData)
console.log(v$.ratings)

const route = useRoute()

const questionnaireA = [
    {
      "type_question": "performance_data_relevance",
      "statement": "This motivational message reflects my achievements and challenges based on my performance data.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "This item measures how well the message aligns with performance reality, following the feedback principles used in motivation enhancement (Deci & Ryan, 2000)."
    },
    {
      "type_question": "message_clarity",
      "statement": "The message I received clearly conveys information about my performance.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "Message clarity is a crucial factor in ensuring that the message is understood and internalized (Guay et al., 2000)."
    },
    {
      "type_question": "emotional_impact",
      "statement": "After reading this message, I feel motivated to improve my performance.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "Measuring emotional impact is related to increasing intrinsic motivation, which is essential for sustainable performance (Deci & Ryan, 2000)."
    },
    {
      "type_question": "actionability",
      "statement": "This message provides clear guidance on actions I can take to improve my performance.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "Assessing whether the message inspires direct behavioral change is a key aspect of evaluating the effectiveness of motivational messages (Guay et al., 2000)."
    },
    {
      "type_question": "overall_satisfaction",
      "statement": "Overall, I am satisfied with the motivational message based on my performance data.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "Overall satisfaction is a frequently used indicator in evaluating motivational interventions (Deci & Ryan, 2000)."
    }
  ];

const questionnaireB = [
    {
      "type_question": "integrated_relevance",
      "statement": "This motivational message is relevant to my performance and also considers my personal characteristics and preferences.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "This item measures how the message integrates performance and personalization data, following the personalized approach proposed in international research (e.g., Hajarian et al., 2019)."
    },
    {
      "type_question": "personalization_quality",
      "statement": "This message feels specifically tailored to me based on my personal data and performance.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "Measuring perceived personalization is essential as research shows that personalized interventions can increase intrinsic motivation (Deci & Ryan, 2000)."
    },
    {
      "type_question": "integration_clarity",
      "statement": "The message I received presents information about performance and personalization data in a clear and understandable way.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "Clarity in integrating both types of data is crucial to ensure that the message is not confusing and is positively received (Guay et al., 2000)."
    },
    {
      "type_question": "emotional_impact_and_motivation",
      "statement": "After reading this message, I feel highly motivated to make the necessary improvements.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "This item assesses the emotional effects of personalized messages, where increased intrinsic motivation is expected when the message reflects the participant's personal condition (Deci & Ryan, 2000)."
    },
    {
      "type_question": "actionability_and_recommendations",
      "statement": "This message provides concrete recommendations that I can apply to improve my performance.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "Assessing actionability is a crucial step in evaluating the practical impact of motivational messages (Guay et al., 2000)."
    },
    {
      "type_question": "overall_satisfaction",
      "statement": "Overall, I am satisfied with the motivational message that combines my performance data and personalization.",
      "min_value": 1,
      "min_label": "Strongly Disagree",
      "max_value": 7,
      "max_label": "Strongly Agree",
      "reason": "Overall satisfaction is an indicator that reflects the acceptance and effectiveness of more complex motivational interventions (Deci & Ryan, 2000)."
    }
  ];

const questions = computed(() => {
  const questionnaire = route.query.type === 'performance_personalization'
    ? questionnaireB
    : questionnaireA

  return questionnaire.map(item => ({
    type: 'rating',
    question: item.statement,
    min: item.min_value,
    max: item.max_value,
    minLabel: item.min_label,
    maxLabel: item.max_label,
    type_question: item.type_question
  }))
})

const isValid = computed(() => {
  // Check all rating questions have values through Vuelidate
  return !v$.value.ratings.$invalid
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
    // Transform form data to requested format
    const result = questions.value.reduce((acc, question) => {
      acc[question.type_question] = {
        statement: question.question,
        ratings: formData.value.ratings[question.type_question]
      }
      return acc
    }, {} as Record<string, { statement: string, ratings: number | null }>)

    try {
      const response = await fetch(`/api/submit-evaluate?exerciseId=${route.params.exerciseId}&type=${route.query.type}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(result, null, 2)
      })

      if (!response.ok) {
        throw new Error('Failed to submit evaluation')
      }

      const exerciseId = route.params.exerciseId || ''
      if (route.query.type === 'performance_personalization') {
        window.location.href = `/thank-you?exerciseId=${exerciseId}`
      } else {
        window.location.href = `/questionnaire/${exerciseId}`
      }
      // window.location.href = `/questionnaire/${exerciseId}`
    } catch (error) {
      console.error('Error submitting evaluation:', error)
      emit('submit-success') // Fallback to original behavior on error
      handleClose()
    }
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
          <h2>Evaluation Form</h2>
          <button 
            class="close-button"
            @click="handleClose"
            aria-label="Close evaluation form"
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
            
            <div v-if="question.type === 'rating'" class="rating-container">
              <div class="rating-labels">
                <span>{{ question.minLabel }}</span>
                <span>{{ question.maxLabel }}</span>
              </div>
              <div class="rating-grid">
                <button
                  v-for="n in question.max"
                  :key="n"
                  :class="['rating-button', { 'selected': formData.ratings[question.type_question] === n }]"
                  @click="formData.ratings[question.type_question] = n"
                  :aria-label="`Rate ${n} out of ${question.max}`"
                >
                  {{ n }}
                </button>
              </div>
            </div>

            <!-- <textarea
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
            </div> -->
          </div>

        </div>

        <div class="modal-footer">
          <button
            class="submit-button"
            @click="submitForm"
            :disabled="!isValid"
            aria-label="Submit feedback"
          >
            Submit Evaluation
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

    .rating-container {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;

      .rating-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        color: #666;
      }

      .rating-grid {
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(40px, 1fr));

        .rating-button {
          padding: 0.8rem;
          border: 2px solid #B1C29E;
          border-radius: 8px;
          background: white;
          color: #666;
          font-weight: bold;
          cursor: pointer;
          transition: all 0.2s ease;
          text-align: center;

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
    
    .rating-container .rating-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
}
</style>