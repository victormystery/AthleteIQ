import { defineStore } from 'pinia'
import { ref } from 'vue'
import userService from '@/services/user.service'
import { useAuthStore } from '@/stores/authStore'
import type { User } from '@/types'

export const useUserStore = defineStore('user', () => {
  const profile = ref<User | null>(null)
  const loading = ref(false)

  async function fetchProfile(): Promise<void> {
    loading.value = true
    try {
      const { data } = await userService.getProfile()
      profile.value = data.data
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(updates: Partial<Pick<User, 'name'>>): Promise<User> {
    const { data } = await userService.updateProfile(updates)
    profile.value = data.data
    // Keep authStore in sync so the sidebar/header name updates immediately
    const authStore = useAuthStore()
    authStore.user = data.data
    return data.data
  }

  return { profile, loading, fetchProfile, updateProfile }
})
