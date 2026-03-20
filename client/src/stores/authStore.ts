import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/auth.service'
import type { User, AuthResponse, RegisterResponse } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken: string | null) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
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
    user.value = data.data.user
    return data.data
  }

  function logout() {
    setToken(null)
    user.value = null
  }

  return { user, token, isAuthenticated, login, register, logout }
})
