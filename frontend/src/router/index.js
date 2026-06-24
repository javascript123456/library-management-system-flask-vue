import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue'), meta: { guest: true } },
  { path: '/', name: 'Layout', component: () => import('@/views/Layout.vue'), meta: { requiresAuth: true }, children: [
      { path: '', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
      { path: 'books', name: 'Books', component: () => import('@/views/Books.vue') },
      { path: 'borrow', name: 'Borrow', component: () => import('@/views/Borrow.vue'), meta: { admin: true } },
      { path: 'my-borrow', name: 'MyBorrow', component: () => import('@/views/MyBorrow.vue') },
      { path: 'users', name: 'Users', component: () => import('@/views/Users.vue'), meta: { admin: true } },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.token) {
    next('/login')
  } else if (to.meta.guest && auth.token) {
    next('/')
  } else if (to.meta.admin && !auth.isAdmin) {
    next('/')
  } else {
    next()
  }
})

export default router
