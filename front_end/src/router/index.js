import { createRouter, createWebHistory } from 'vue-router'
import SendUpdate from '@/views/SendUpdate.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: SendUpdate
    },
  ]
})

export default router
