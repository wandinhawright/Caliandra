import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CartView from '../views/CartView.vue'
import CatalogView from '../views/CatalogView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import BlogView from '../views/BlogView.vue'
import VerificationView from '../views/VerificationView.vue'
import FinalizationView from '../views/FinalizationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/catalogo',
      name: 'catalogo',
      component: CatalogView
    },
    {
      path: '/carrinho',
      name: 'carrinho',
      component: CartView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { hideHeader: true }
    },
    {
      path: '/registro',
      name: 'registro',
      component: RegisterView,
      meta: { hideHeader: true }
    },
    {
      path: '/verificacao',
      name: 'verificacao',
      component: VerificationView,
      meta: { hideHeader: true }
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/blog',
      name: 'blog',
      component: BlogView
    },
    {
      path: '/finalizacao',
      name: 'finalizacao',
      component: FinalizationView,
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard for auth
router.beforeEach((to, from, next) => {
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    // TODO: Implement proper auth check
    // For now, just allow navigation
    next()
  } else {
    next()
  }
})

export default router
