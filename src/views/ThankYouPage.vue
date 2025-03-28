<template>
  <div class="thank-you-page">
    <div class="language-button-container">
      <button @click="changeLanguage" class="btn btn-outline-secondary language-button">
        {{ currentLanguage === 'en' ? '日本語' : 'English' }}
      </button>
    </div>
    <div class="thank-you-card">
      <div class="bowing-figure animate__animated animate__fadeIn"></div>
      <div class="messages">
        <h1 class="animate__animated animate__fadeIn">{{ messages[currentLanguage].title }}</h1>
        <p class="animate__animated animate__fadeIn animate__delay-1s">{{ messages[currentLanguage].message }}</p>
      </div>
      <div v-if="showGraduationMessage" class="flip-container">
        <!-- <div class="bowing-figure animate__animated animate__fadeIn"></div> -->
        <div class="flip-card" @click="flipped = !flipped" :class="{ flipped: flipped }">
          <div class="flip-card-inner">
            <div class="flip-card-front">
              <!-- <div class="bowing-figure animate__animated animate__fadeIn"></div> -->
              <div class="flip-hint animate__animated animate__pulse animate__infinite">
                ✨ Click to view special message ✨
              </div>
            </div>
            <div class="flip-card-back">
              <div class="messages">
                <h2>{{ messages[currentLanguage].graduation.title }}</h2>
                <p>{{ messages[currentLanguage].graduation.message }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import confetti from 'canvas-confetti'
import { useRoute } from 'vue-router'

const currentLanguage = ref('en')

const messages = {
  en: {
    title: 'Thank You!',
    message: 'Thank you so much for participating in this experiment! 🙌 Your support and contributions mean a lot to us. We hope you find this experience useful, and we wish you good health and success in the future. 🌟🙏',
    graduation: {
      title: 'Congraduations!',
      message: 'Thank you so much for all your help and support during our studies at Tokyo Metropolitan University. 🙏✨ Wishing you success in your next journey. Hope to see you again in the future! 🤝🌏'
    }
  },
  ja: {
    title: 'ありがとうございます',
    message: 'この実験に参加してくれて本当にありがとう！🙌 皆様のご支援とご協力は、私たちにとって大きな意味があります。今回の実験が皆様のお役に立つことを願っております。🌟🙏',
    graduation: {
      title: '卒業おめでとうございます！',
      message: '東京都市大学での研究期間中、多大なるご支援とご協力をいただき、誠にありがとうございました。🙏✨ 今後のご活躍を心よりお祈り申し上げます。またお会いできる日を楽しみにしております！🤝🌏'
    }
  }
}

const specialExerciseIds = new Set(['GIityqPpa92j2YrRy9Hd', 'T4as4G3Z5PQuU81OpRvb', 'cNINMWMzYUHoKwYf0xBP', 'AQje8woJhWLNpYCVD74y'])
const urlParams = new URLSearchParams(window.location.search)
const route = useRoute()
const exerciseId = route.query.exerciseId
const showGraduationMessage = exerciseId && specialExerciseIds.has(exerciseId)
const flipped = ref(false)

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
  position: relative;
}

.card-container {
  perspective: 1000px;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.thank-you-card {
  text-align: center;
  padding: 3rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.8s;
  backface-visibility: hidden;
}

.front {
  transform: rotateY(0deg);
}

.back {
  position: absolute;
  top: 0;
  left: 0;
  transform: rotateY(180deg);
}

.show-graduation .front {
  transform: rotateY(-180deg);
}

.show-graduation .back {
  transform: rotateY(0deg);
}

.flip-container {
  perspective: 1000px;
  width: 100%;
  margin-top: 2rem;
}

.flip-hint {
  text-align: center;
  color: #ff6b6b;
  font-weight: 600;
  animation-duration: 2s;
  margin-bottom: 1rem;
}

.flip-card {
  background-color: transparent;
  width: 100%;
  height: 300px;
  cursor: pointer;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.8s;
  transform-style: preserve-3d;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.flip-card.flipped .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  padding: 2rem;
  background-color: #fff;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.flip-card-back {
  transform: rotateY(180deg);
  
  h2 {
    color: #d35400;
    margin-bottom: 1rem;
  }
  
  p {
    color: #666;
    line-height: 1.6;
  }
}

.flip-hint {
  color: #ff6b6b;
  font-weight: 600;
  margin-top: 1rem;
  animation-duration: 2s;
}

.thank-you-card {
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

.language-button-container {
  position: absolute;
  top: 2rem;
  right: 2rem;
  z-index: 10;
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