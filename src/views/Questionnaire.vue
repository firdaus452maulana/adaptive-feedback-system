<script setup lang="ts">
import { useRoute } from 'vue-router'
import MultiQuestionnaireForm from '../components/MultiQuestionnaireForm.vue'

const route = useRoute()
console.log('Questionnaire slug:', route.params.exerciseId)
</script>

<template>
  <div class="questionnaire-page">
    <MultiQuestionnaireForm />
  </div>
</template>

<style lang="scss" scoped>
.questionnaire-page {
  min-height: 100vh;
  background-color: #FCE7C8;
  padding: 2rem;
}
</style>