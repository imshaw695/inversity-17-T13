import { createRouter, createWebHistory } from 'vue-router'
import CrudView from '../views/CrudView.vue'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import PasswordResetView from '../views/PasswordResetView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/index',
      name: 'index',
      component: HomeView
    },
    {
      path: '/crud',
      name: 'crud',
      component: CrudView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/passwordresetview',
      name: 'passwordreset',
      component: PasswordResetView,
    },
  ]
})

export default router
