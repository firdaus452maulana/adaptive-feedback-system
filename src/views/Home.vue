<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const startQuestionnaire = () => {
  router.push('/questionnaire')
}
</script>

<template>
  <div class="home">
    <div class="hero-section">
      <h1>Adaptive Feedback System</h1>
      <p class="lead">
        Help us understand your exercise habits and preferences to provide better recommendations.
      </p>
      <button @click="startQuestionnaire" class="btn btn-primary btn-lg" disabled>
        Start Questionnaire
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "sass:color";
.home {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #FCE7C8;
  
  .hero-section {
    text-align: center;
    padding: 3rem;
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin: 0 2rem;
    
    h1 {
      color: #333;
      margin-bottom: 1.5rem;
    }
    
    .lead {
      color: #666;
      margin-bottom: 2rem;
    }
    
    .btn-primary {
      background-color: color.adjust(#B1C29E, $lightness: -10%);
      border-color: #B1C29E;
      padding: 1rem 2rem;
      
      &:hover {
        background-color: color.adjust(#B1C29E, $lightness: -10%);
      }
    }
  }
}
</style>