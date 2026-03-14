import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: "/:catchAll(.*)",
      name: "notfound",
      component: () => import(/* webpackChunkName: "notfound" */ "@/views/NotFound.vue"),
      meta: {
        pageTitle: "找不到頁面"
      }
    }
  ],
})

export default router
