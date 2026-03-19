import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

export function useAuth() {
  const authStore = useAuthStore()
  const router = useRouter()

  async function login(credentials: { email: string; password: string }) {
    await authStore.login(credentials)
    await router.push({ name: 'Dashboard' })
  }

  async function logout() {
    authStore.logout()
    await router.push({ name: 'Login' })
  }

  return {
    login,
    logout,
    isAuthenticated: computed(() => authStore.isAuthenticated),
    user: computed(() => authStore.user)
  }
}
