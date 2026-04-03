import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/auth.service'
import userService from '@/services/user.service'
import type { User, AuthResponse, RegisterResponse } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const initializing = ref(false)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  function setToken(newToken: string | null) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  /**
   * Rehydrate user data from a persisted token.
   * Called once on app initialization so sidebar, header, etc. show the user info.
   */
  async function initialize(): Promise<void> {
    if (!token.value || user.value) return
    initializing.value = true
    try {
      const { data } = await userService.getProfile()
      user.value = data.data
    } catch {
      // Token is invalid / expired — clear it
      setToken(null)
      user.value = null
    } finally {
      initializing.value = false
    }
  }

  async function login(credentials: { email: string; password: string }): Promise<AuthResponse> {
    const { data } = await authService.login(credentials)
    setToken(data.data.token)
    user.value = data.data.user
    return data.data
  }

  async function register(userData: { name: string; email: string; password: string }): Promise<RegisterResponse> {
    const { data } = await authService.register(userData)
    // Server does NOT return a token on register — the user must log in afterwards
    user.value = data.data.user
    return data.data
  }

  async function loginWithToken(rawToken: string): Promise<void> {
    user.value = null
    setToken(rawToken)
    await initialize()
  }

  async function loginWithGoogleCode(code: string): Promise<void> {
    const { data } = await authService.exchangeGoogleCode(code)
    setToken(data.data.token)
    user.value = data.data.user
  }

  function logout() {
    setToken(null)
    user.value = null
  }

  return {
    user,
    token,
    initializing,
    isAuthenticated,
    isAdmin,
    initialize,
    login,
    loginWithToken,
    loginWithGoogleCode,
    register,
    logout
  }
})
