<template>
  <div class="flex flex-col items-center justify-center py-16 gap-4">
    <AppSpinner size="lg" color="primary" />
    <p class="text-sm text-slate-500">Signing you in…</p>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useToast } from '@/composables/useToast'
import AppSpinner from '@/components/AppSpinner.vue'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

onMounted(async () => {
  const params = new URLSearchParams(window.location.search)
  const code = params.get('code')
  const token = params.get('token')
  const error = params.get('error')

  if (error || (!code && !token)) {
    toast.error('Google sign-in failed. Please try again.')
    router.replace({ name: 'Login' })
    return
  }

  try {
    if (code) {
      await authStore.loginWithGoogleCode(code)
    } else if (token) {
      // Backward compatibility with older callback URLs.
      await authStore.loginWithToken(token)
    }
    toast.success('Signed in with Google!')
    router.replace({ name: authStore.isAdmin ? 'AdminDashboard' : 'Dashboard' })
  } catch {
    toast.error('Authentication failed. Please try again.')
    router.replace({ name: 'Login' })
  }
})
</script>
