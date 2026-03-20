<template>
  <div class="flex flex-col gap-6 flex-1">
    <div>
      <h1 class="text-2xl font-bold text-slate-800">Create your account</h1>
      <p class="text-sm text-slate-500 mt-1">Start tracking your performance today</p>
    </div>

    <BaseAlert v-if="error" type="error" :show="!!error" dismissible @dismiss="error = ''">
      {{ error }}
    </BaseAlert>

    <form @submit.prevent="handleRegister" class="flex flex-col gap-4" novalidate>
      <BaseInput
        v-model="form.name"
        label="Full name"
        type="text"
        placeholder="Jane Smith"
        autocomplete="name"
        :error="errors.name"
        required
        @blur="validateField('name')"
      />
      <BaseInput
        v-model="form.email"
        label="Email"
        type="email"
        placeholder="you@example.com"
        autocomplete="email"
        :error="errors.email"
        required
        @blur="validateField('email')"
      />
      <div class="relative">
        <BaseInput
          v-model="form.password"
          label="Password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="At least 8 characters"
          autocomplete="new-password"
          hint="Minimum 8 characters"
          :error="errors.password"
          required
          @blur="validateField('password')"
        />
        <button
          type="button"
          class="absolute right-3 bottom-2.5 text-slate-400 hover:text-slate-600 transition-colors"
          @click="showPassword = !showPassword"
          :aria-label="showPassword ? 'Hide password' : 'Show password'"
        >
          <svg v-if="showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
        </button>
      </div>

      <BaseButton type="submit" :loading="loading" :block="true" class="mt-2">
        Create account
      </BaseButton>
    </form>

    <p class="text-center text-sm text-slate-500 mt-auto">
      Already have an account?
      <router-link to="/auth/login" class="text-primary-600 font-medium hover:underline">Sign in</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { isEmail, required, minLength } from '@/utils/validators'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseAlert from '@/components/BaseAlert.vue'

const authStore = useAuthStore()
const router = useRouter()

const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

const form = reactive({ name: '', email: '', password: '' })
const errors = reactive({ name: '', email: '', password: '' })

function validateField(field: 'name' | 'email' | 'password') {
  if (field === 'name') {
    errors.name = required(form.name) ? '' : 'Name is required'
  }
  if (field === 'email') {
    if (!required(form.email)) errors.email = 'Email is required'
    else if (!isEmail(form.email)) errors.email = 'Enter a valid email'
    else errors.email = ''
  }
  if (field === 'password') {
    if (!required(form.password)) errors.password = 'Password is required'
    else if (!minLength(8)(form.password)) errors.password = 'At least 8 characters required'
    else errors.password = ''
  }
}

function validateAll(): boolean {
  validateField('name')
  validateField('email')
  validateField('password')
  return !errors.name && !errors.email && !errors.password
}

async function handleRegister() {
  if (!validateAll()) return
  loading.value = true
  error.value = ''
  try {
    await authStore.register(form)
    await router.push({ name: 'Login' })
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { message?: string } } }
    error.value = axiosErr.response?.data?.message ?? 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
