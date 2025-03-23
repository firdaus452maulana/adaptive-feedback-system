<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

const props = defineProps<{
  questions: Array<{
    type: string
    question: string
    options?: string[]
    min?: number
    max?: number
    minLabel?: string
    maxLabel?: string
  }>
  answers: {
    multipleChoice: string
    multipleChoiceOther: string
    checkboxes: string[]
    checkboxOther: string
    scale: number
    shortAnswer: string
  }
}>()

const emit = defineEmits(['editQuestion'])

const getFormattedAnswer = (type: string, index: number) => {
  switch (type) {
    case 'multiple-choice':
      return props.answers.multipleChoice === 'Other'
        ? props.answers.multipleChoiceOther
        : props.answers.multipleChoice
    case 'checkbox':
      const answers = [...props.answers.checkboxes]
      if (answers.includes('Other')) {
        answers.splice(answers.indexOf('Other'), 1)
        answers.push(props.answers.checkboxOther)
      }
      return answers.join(', ')
    case 'scale':
      return `${props.answers.scale} / 7`
    case 'short-answer':
      return props.answers.shortAnswer
    default:
      return ''
  }
}
</script>

<template>
  <div class="review-page">
    <h2 class="review-title">Review Your Answers</h2>
    <p class="review-subtitle">Please review your answers before submitting. Click on any question to edit your response.</p>

    <div class="answers-list">
      <div 
        v-for="(question, index) in questions" 
        :key="index"
        class="answer-card"
        @click="emit('editQuestion', index)"
      >
        <div class="answer-header">
          <span class="question-number">Question {{ index + 1 }}</span>
          <button class="edit-button">
            <i class="fas fa-edit"></i>
            Edit
          </button>
        </div>
        
        <h3 class="question-text">{{ question.question }}</h3>
        
        <div class="answer-content">
          <p class="answer-text">{{ getFormattedAnswer(question.type, index) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "sass:color";
.review-page {
  padding: 1rem;

  .review-title {
    color: #333;
    font-size: 1.75rem;
    margin-bottom: 0.5rem;
    text-align: center;
  }

  .review-subtitle {
    color: #666;
    text-align: center;
    margin-bottom: 2rem;
  }

  .answers-list {
    display: grid;
    gap: 1rem;

    .answer-card {
      background-color: #fff;
      border: 2px solid #B1C29E;
      border-radius: 8px;
      padding: 1.5rem;
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .answer-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;

        .question-number {
          font-weight: 600;
          color: #F0A04B;
        }

        .edit-button {
          background: none;
          border: none;
          color: #B1C29E;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.9rem;
          padding: 0;

          &:hover {
            color: color.adjust(#B1C29E, $lightness: -10%);
          }

          i {
            font-size: 1rem;
          }
        }
      }

      .question-text {
        color: #333;
        font-size: 1.1rem;
        margin-bottom: 1rem;
      }

      .answer-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 4px;

        .answer-text {
          margin: 0;
          color: #666;
        }
      }
    }
  }
}
</style>