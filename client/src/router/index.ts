import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Landing',
    component: () => import('@/pages/LandingPage.vue')
  },
  {
    path: '/app',
    component: () => import('@/layouts/DefaultLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/pages/DashboardPage.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/pages/ProfilePage.vue')
      },
      {
        path: 'questionnaire',
        name: 'Questionnaire',
        component: () => import('@/pages/QuestionnairePage.vue')
      },
      {
        path: 'results',
        name: 'Results',
        component: () => import('@/pages/ResultsPage.vue')
      },
      {
        path: 'pathways',
        name: 'Pathways',
        component: () => import('@/pages/PathwaysPage.vue')
      },
      {
        path: 'pathways/:slug',
        name: 'PathwayDetail',
        component: () => import('@/pages/PathwayDetailPage.vue')
      },
      {
        path: 'roadmap/:slug',
        name: 'Roadmap',
        component: () => import('@/pages/RoadmapPage.vue')
      },
      {
        path: 'feedback',
        name: 'Feedback',
        component: () => import('@/pages/FeedbackPage.vue')
      }
    ]
  },
  {
    path: '/admin',
    component: () => import('@/layouts/DefaultLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/pages/admin/AdminDashboardPage.vue')
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/pages/admin/AdminUsersPage.vue')
      }
    ]
  },
  {
    path: '/auth',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/pages/LoginPage.vue')
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('@/pages/RegisterPage.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/pages/NotFoundPage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()

  // Rehydrate user data from persisted token on first navigation
  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.initialize()
  }

  // Redirect authenticated users away from landing / auth pages to dashboard
  if ((to.name === 'Landing' || to.path.startsWith('/auth')) && authStore.isAuthenticated) {
    next({ name: authStore.isAdmin ? 'AdminDashboard' : 'Dashboard' })
    return
  }

  // Require authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login' })
    return
  }

  // Require admin role
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next({ name: 'Dashboard' })
    return
  }

  next()
})

export default router
