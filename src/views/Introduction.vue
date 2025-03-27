<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const exerciseId = route.query.exerciseId
</script>
<template>
  <div class="introduction">
    <h1>🎉 Hey there! 🎉</h1>
    
    <div class="steps-container">
      <div class="step">
        <p>We have some exciting information for you about your previous squat performance analysis. You'll be receiving messages like:</p>
        <ul>
          <li><strong>Feedback</strong></li>
          <li><strong>Motivation</strong></li>
          <li><strong>Safety Notes</strong></li>
          <li><strong>Suggestion</strong></li>
        </ul>
      </div>

      <div class="step">
        <h2><span class="emoji">📝</span> <strong>Here's what you need to do:</strong></h2>
        <ol>
          <li><strong>Check out the messages:</strong> Visit the page where you'll see all the messages we've prepared for you.</li>
          <li><strong>Fill out the personalization questionnaire:</strong> Complete the questionnaire so we can tailor the analysis specifically to your needs.</li>
          <li><strong>Review the messages again:</strong> Take a moment to go through the messages once more.</li>
        </ol>
      </div>

      <div class="support">
        <p>Thank you so much for being a part of this experiment and for taking the time to participate in all these activities! <span class="emoji">🙏😊</span></p>
        <p><span class="emoji">😊</span> If you run into any issues or have questions, feel free to contact anytime! <span class="emoji">👍</span></p>
        <p>Have fun, and hope you have an amazing day! <span class="emoji">🌟</span></p>
      </div>

      <div class="start-button-container">
        <router-link :to="`/feedback/${exerciseId}?type=performance`" class="start-button">
          <span class="emoji">🚀</span> Let's Start!
        </router-link>
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
</style>