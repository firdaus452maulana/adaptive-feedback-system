import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Questionnaire from '../views/Questionnaire.vue'
import Results from '../views/Results.vue'
import CombinedFeedback from '../components/CombinedFeedback.vue'
import ThankYouPage from '../views/ThankYouPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/questionnaire/:exerciseId',
      name: 'Questionnaire',
      component: Questionnaire,
      props: true
    },
    {
      path: '/results',
      name: 'Results',
      component: Results
    },
    {
      path: '/feedback/:exerciseId',
      name: 'Feedback',
      component: CombinedFeedback,
      props: true
    },
    {
      path: '/thank-you',
      name: 'ThankYou',
      component: ThankYouPage
    }
  ]
})

export default router