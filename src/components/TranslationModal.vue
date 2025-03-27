<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const exerciseId = route.query.exerciseId
const currentLang = ref('en')

const emit = defineEmits(['close'])

const handleClose = () => {
  emit('close')
}

const handleBackdropClick = (event: MouseEvent) => {
  if ((event.target as HTMLElement).classList.contains('modal-backdrop')) {
    handleClose()
  }
}

const toggleLanguage = () => {
  currentLang.value = currentLang.value === 'en' ? 'ja' : 'en'
}

const translations = {
  en: {
    title: "Browser Translation Help",
    intro: "To help understand the content better, you can use your browser's built-in translation feature:",
    chrome: "Chrome/Edge:",
    chromeStep1: "Right-click anywhere on the page",
    chromeStep2: "Select \"Translate to [your language]\"",
    firefox: "Firefox:",
    firefoxStep1: "Install a translation extension like \"Google Translate\"",
    firefoxStep2: "Right-click and select \"Translate this page\"",
    safari: "Safari:",
    safariStep1: "Install a translation extension from the App Store",
    safariStep2: "Use the extension to translate the page",
    continue: "Continue ->"
  },
  ja: {
    title: "ブラウザ翻訳ヘルプ",
    intro: "コンテンツをより理解しやすくするために、ブラウザの組み込み翻訳機能を使用できます:",
    chrome: "Chrome/Edge:",
    chromeStep1: "ページの任意の場所を右クリック",
    chromeStep2: "\"[言語]に翻訳\"を選択",
    firefox: "Firefox:",
    firefoxStep1: "\"Google翻訳\"などの翻訳拡張機能をインストール",
    firefoxStep2: "右クリックして\"このページを翻訳\"を選択",
    safari: "Safari:",
    safariStep1: "App Storeから翻訳拡張機能をインストール",
    safariStep2: "拡張機能を使用してページを翻訳",
    continue: "進む ->"
  }
}
</script>

<template>
  <Transition name="modal">
    <div
      class="modal-backdrop"
      @click="handleBackdropClick"
      role="dialog"
      aria-modal="true"
    >
      <div class="modal-container">
        <div class="modal-header">
          <div class="modal-header-content">
            <h2>{{ translations[currentLang].title }}</h2>
            <button
              @click="toggleLanguage"
              class="lang-button"
            >
              {{ currentLang === 'en' ? '日本語' : 'English' }}
            </button>
          </div>
          <button
            class="close-button"
            @click="handleClose"
            aria-label="Close translation help"
          >
            &times;
          </button>
        </div>

        <div class="modal-content">
          <div class="translation-instructions">
            <p>{{ translations[currentLang].intro }}</p>
            
            <div class="instruction-step">
              <h3>{{ translations[currentLang].chrome }}</h3>
              <ol>
                <li>{{ translations[currentLang].chromeStep1 }}</li>
                <li>{{ translations[currentLang].chromeStep2 }}</li>
              </ol>
            </div>

            <div class="instruction-step">
              <h3>{{ translations[currentLang].firefox }}</h3>
              <ol>
                <li>{{ translations[currentLang].firefoxStep1 }}</li>
                <li>{{ translations[currentLang].firefoxStep2 }}</li>
              </ol>
            </div>

            <div class="instruction-step">
              <h3>{{ translations[currentLang].safari }}</h3>
              <ol>
                <li>{{ translations[currentLang].safariStep1 }}</li>
                <li>{{ translations[currentLang].safariStep2 }}</li>
              </ol>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <router-link
            :to="`/feedback/${exerciseId}?type=performance`"
            class="continue-button"
            @click="handleClose"
          >
            {{ translations[currentLang].continue }}
          </router-link>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
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
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
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
}
.close-button:hover {
  color: #333;
}

.modal-header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.lang-button {
  padding: 0.25rem 0.75rem;
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

.modal-content {
  padding: 1.5rem;
  overflow-y: auto;
  flex-grow: 1;
}

.instruction-step {
  margin-bottom: 1.5rem;
}

.instruction-step h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.instruction-step ol {
  padding-left: 1.5rem;
  margin: 0;
}

.instruction-step li {
  margin-bottom: 0.5rem;
}

.continue-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #42b983;
  color: white;
  border-radius: 6px;
  text-decoration: none;
  transition: all 0.2s;
}

.continue-button:hover {
  background-color: #3aa876;
}

.modal-content {
  padding: 1.5rem;
  overflow-y: auto;
}

.translation-instructions {
  padding: 1rem;
}

.instruction-step {
  margin-bottom: 1.5rem;
}

.instruction-step h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #eee;
  text-align: center;
}

.continue-button {
  background-color: #42b983;
  color: white;
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 2rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-block;
}

.continue-button:hover {
  background-color: #3aa876;
  transform: translateY(-1px);
}
</style>