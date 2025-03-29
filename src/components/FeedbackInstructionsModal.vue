<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])

const feedbackType = computed(() => {
  return route.query.type || 'performance'
})

const instructions = computed(() => {
  if (feedbackType.value === 'performance_personalization') {
    return {
      title: 'Personalized Feedback Instructions',
      content: [
        'This page contains your squat performance analysis with feedback tailored to your profile. Content structure:',
        '1. Squat performance analysis table',
        '2. 4 personalized messages: Feedback (specific analysis), Motivation (customized), Safety Notes (condition tips), Suggestion (personalized exercises)',
        '3. Evaluation form to rate this feedback',
        'Please review the personalized messages, then complete the evaluation form.'
      ]
    }
  } else {
    return {
      title: 'Standard Feedback Instructions',
      content: [
        'This page contains your squat performance analysis. Content structure:',
        '1. Squat performance analysis table',
        '2. 4 standard messages: Feedback (general analysis), Motivation (standard), Safety Notes (general tips), Suggestion (common exercises)',
        '3. Evaluation form to rate this feedback',
        'Please review the messages, then complete the evaluation form.'
      ]
    }
  }
})
</script>

<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-container">
      <div class="modal-header">
        <h3>{{ instructions.title }}</h3>
        <button @click="emit('close')" class="close-button">
          ×
        </button>
      </div>
      
      <div class="modal-content">
        <ul>
          <li
            v-for="(item, index) in instructions.content"
            :key="index"
            :class="[1,2,3].includes(index) ? 'center-bold' : 'left-normal'"
          >
            {{ item }}
          </li>
        </ul>
      </div>
      
      <div class="modal-footer">
        <button @click="emit('close')" class="btn btn-primary">
          Got It
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-container {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transform: translateY(20px);
  animation: slideUp 0.3s ease-out forwards;
}

@keyframes slideUp {
  to { transform: translateY(0); }
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #F0A04B;
  color: white;
  border-radius: 12px 12px 0 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.75rem;
  cursor: pointer;
  color: white;
  transition: transform 0.2s ease;
  padding: 0.75rem;
}

.close-button:hover {
  transform: scale(1.1);
  color: #f8f8f8;
}

.modal-content {
  padding: 1.5rem;
  font-size: 1rem;
  line-height: 1.6;
  color: #444;
  text-align: left;
}

.highlight {
  color: #F0A04B;
  font-weight: 600;
}

.modal-content ul {
  padding-left: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.modal-content li {
  margin-bottom: 0.75rem;
  padding-left: 0;
  list-style-type: none;
  position: relative;
}

.modal-content li.center-bold {
  text-align: center;
  font-weight: 700;
}

.modal-content li.left-normal {
  text-align: left;
  font-weight: 500;
}

.modal-content li:first-letter {
  text-transform: uppercase;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: #B1C29E;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #9aae85;
}
</style>