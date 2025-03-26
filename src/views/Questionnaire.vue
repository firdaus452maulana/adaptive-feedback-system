<script setup lang="ts">
import { useRoute } from 'vue-router'
import QuestionnaireForm from '../components/QuestionnaireForm.vue'

const route = useRoute()
console.log('Questionnaire slug:', route.params.slug)
</script>

<template>
  <div class="questionnaire-page">
    <QuestionnaireForm />
  </div>
</template>

<style lang="scss" scoped>
.questionnaire-page {
  min-height: 100vh;
  background-color: #FCE7C8;
  padding: 2rem;
}
</style>