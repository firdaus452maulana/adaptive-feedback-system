<template>
  <div class="thank-you-page">
    <div class="thank-you-card">
      <div class="bowing-figure animate__animated animate__fadeIn"></div>
      <div class="messages">
        <h1 class="animate__animated animate__fadeIn">{{ messages[currentLanguage].title }}</h1>
        <p class="animate__animated animate__fadeIn animate__delay-1s">{{ messages[currentLanguage].message }}</p>
      </div>
      <button @click="changeLanguage" class="btn btn-outline-secondary language-button">
        {{ currentLanguage === 'en' ? '日本語' : 'English' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import confetti from 'canvas-confetti'

const currentLanguage = ref('en')

const messages = {
  en: {
    title: 'Thank You!',
    message: 'We appreciate your time and effort.'
  },
  ja: {
    title: 'ありがとうございます',
    message: 'ご協力いただき誠にありがとうございます。'
  }
}

const changeLanguage = () => {
  currentLanguage.value = currentLanguage.value === 'en' ? 'ja' : 'en'
}

const fireConfetti = () => {
  confetti({
    particleCount: 100,
    spread: 70,
    origin: { y: 0.6 }
  })
}

onMounted(() => {
  fireConfetti()
})
</script>

<style lang="scss" scoped>
@use "sass:color";
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

.thank-you-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #FCE7C8;
  padding: 2rem;
  font-family: 'Poppins', sans-serif;
}

.thank-you-card {
  text-align: center;
  padding: 3rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  width: 100%;
  margin: 0 auto;

  h1 {
    color: #333;
    margin-bottom: 1.5rem;
    font-size: 2.5rem;
    font-weight: 700;
  }

  p {
    color: #666;
    margin-bottom: 2rem;
    font-size: 1.25rem;
    font-weight: 400;
  }
}

.bowing-figure {
  width: 100px;
  height: 100px;
  margin: 0 auto 2rem;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    width: 60px;
    height: 60px;
    background-color: #333;
    border-radius: 50%;
    left: 20px;
    top: 0;
  }
  
  &::after {
    content: '';
    position: absolute;
    width: 80px;
    height: 40px;
    background-color: #333;
    border-radius: 20px;
    left: 10px;
    top: 60px;
    animation: bow 2s infinite alternate;
    transform-origin: top center;
  }
}

@keyframes bow {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(20deg);
  }
}

.language-button {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-weight: 600;

  &:hover {
    transform: scale(1.05);
  }
}

/* Animation classes */
.animate__animated {
  animation-duration: 1s;
  animation-fill-mode: both;
}

.animate__fadeIn {
  animation-name: fadeIn;
}

.animate__delay-1s {
  animation-delay: 1s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .thank-you-card {
    padding: 2rem 1.5rem;
    
    h1 {
      font-size: 2rem;
    }
    
    p {
      font-size: 1.1rem;
    }
  }
  
  .bowing-figure {
    width: 80px;
    height: 80px;
    margin-bottom: 1.5rem;
    
    &::before {
      width: 50px;
      height: 50px;
      left: 15px;
    }
    
    &::after {
      width: 60px;
      height: 30px;
      left: 10px;
      top: 50px;
    }
  }
}
</style>