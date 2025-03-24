import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Questionnaire from '../views/Questionnaire.vue'
import Results from '../views/Results.vue'
import CombinedFeedback from '../components/CombinedFeedback.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/questionnaire',
      name: 'Questionnaire',
      component: Questionnaire
    },
    {
      path: '/results',
      name: 'Results',
      component: Results
    },
    {
      path: '/feedback',
      name: 'Feedback',
      component: CombinedFeedback
    }
  ]
})

export default router