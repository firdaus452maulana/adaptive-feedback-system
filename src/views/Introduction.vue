<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ref } from 'vue'
import TranslationModal from '../components/TranslationModal.vue'

const route = useRoute()
const exerciseId = route.query.exerciseId
const showModal = ref(false)
const currentLang = ref('en')

const handleStartClick = () => {
  showModal.value = true
}

const toggleLanguage = () => {
  currentLang.value = currentLang.value === 'en' ? 'ja' : 'en'
}

const translations = {
  en: {
    title: "🎉 Hey there! 🎉",
    intro: "After performing a previously performed squat, we have some interesting information for you about analyzing your previous squat performance. You will receive messages like:",
    feedback: "Feedback",
    motivation: "Motivation",
    safety: "Safety Notes",
    suggestion: "Suggestion",
    whatToDo: "Here's what you need to do:",
    step1: "Review the messages: After this you will visit a page that analyzes the performance of your squats and you will also see all the messages we have prepared for you.",
    step2: "Fill out the personalization questionnaire: Complete the questionnaire so we can tailor the analysis specifically to your needs.",
    step3: "Review the messages again: You will revisit the squat performance analysis page. Take a moment to read through the messages once again.",
    thankYou: "Thank you so much for being a part of this experiment and for taking the time to participate in all these activities! 🙏😊",
    contact: "😊 If you run into any issues or have questions, feel free to contact anytime! 👍",
    haveFun: "Have fun, and hope you have an amazing day! 🌟",
    startButton: "Let's Start!"
  },
  ja: {
    title: "🎉 こんにちは！ 🎉",
    intro: "以前行ったスクワットを行った後、以前のスクワットのパフォーマンスを分析する興味深い情報があります。というようなメッセージが表示されます：",
    feedback: "フィードバック",
    motivation: "モチベーション",
    safety: "安全上の注意",
    suggestion: "提案",
    whatToDo: "以下の手順に従ってください:",
    step1: "メッセージを確認: この後、スクワットのパフォーマンスを分析するページが表示され、私たちが用意したすべてのメッセージが表示されます。",
    step2: "個人設定アンケートに記入: 分析をあなたのニーズに合わせて調整できるようにアンケートに回答してください。",
    step3: "メッセージを再度確認: スクワットのパフォーマンス分析のページをもう一度ご覧ください。もう一度メッセージに目を通してください。",
    thankYou: "この実験に参加し、すべての活動に時間を割いていただき、本当にありがとうございます！ 🙏😊",
    contact: "😊 問題が発生した場合や質問がある場合は、いつでもお気軽にご連絡ください！ 👍",
    haveFun: "楽しんで、素晴らしい一日をお過ごしください！ 🌟",
    startButton: "始めましょう！"
  }
}
</script>
<template>
  <div class="introduction">
    <div class="language-toggle">
      <button @click="toggleLanguage" class="lang-button">
        {{ currentLang === 'en' ? '日本語' : 'English' }}
      </button>
    </div>
    
    <h1>{{ translations[currentLang].title }}</h1>
    
    <div class="steps-container">
      <div class="step">
        <p>{{ translations[currentLang].intro }}</p>
        <ul>
          <li><strong>{{ translations[currentLang].feedback }}</strong></li>
          <li><strong>{{ translations[currentLang].motivation }}</strong></li>
          <li><strong>{{ translations[currentLang].safety }}</strong></li>
          <li><strong>{{ translations[currentLang].suggestion }}</strong></li>
        </ul>
      </div>

      <div class="step">
        <h2><span class="emoji">📝</span> <strong>{{ translations[currentLang].whatToDo }}</strong></h2>
        <ol>
          <li><strong>{{ translations[currentLang].step1.split(':')[0] }}:</strong> {{ translations[currentLang].step1.split(':')[1] }}</li>
          <li><strong>{{ translations[currentLang].step2.split(':')[0] }}:</strong> {{ translations[currentLang].step2.split(':')[1] }}</li>
          <li><strong>{{ translations[currentLang].step3.split(':')[0] }}:</strong> {{ translations[currentLang].step3.split(':')[1] }}</li>
        </ol>
      </div>

      <div class="support">
        <p>{{ translations[currentLang].thankYou }}</p>
        <p>{{ translations[currentLang].contact }}</p>
        <p>{{ translations[currentLang].haveFun }}</p>
      </div>

      <div class="start-button-container">
        <button @click="handleStartClick" class="start-button">
          <span class="emoji">🚀</span> {{ translations[currentLang].startButton }}
        </button>
        <TranslationModal
          v-if="showModal"
          @close="showModal = false"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Introduction',
});
</script>

<style scoped>
.introduction {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.steps-container {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 2rem;
}

.step {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}

.step:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

h2 {
  color: #42b983;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.emoji {
  margin-right: 10px;
  font-size: 1.2em;
}

ul {
  padding-left: 1.5rem;
}

li {
  margin-bottom: 0.5rem;
}

.support {
  margin-top: 2rem;
  padding: 1rem;
  background: #e8f4fc;
  border-radius: 8px;
  text-align: center;
}

.start-button-container {
  text-align: center;
  margin-top: 2rem;
}

.start-button {
  padding: 1rem 2rem;
  background-color: #42b983;
  color: white;
  border-radius: 6px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.2s;
  font-size: 1.1rem;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.start-button:hover {
  background-color: #3aa876;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.language-toggle {
  text-align: right;
  margin-bottom: 1rem;
}

.lang-button {
  padding: 0.5rem 1rem;
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.lang-button:hover {
  background-color: #e0e0e0;
  border-color: #ccc;
}
</style>