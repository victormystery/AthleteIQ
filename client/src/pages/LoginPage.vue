<template>
  <div ref="pageRef" class="flex flex-col gap-5 flex-1">
    <!-- Header -->
    <div>
      <div ref="iconRef" class="auth-icon-wrap">
        <div class="auth-icon-glow"></div>
        <div class="auth-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5">
            <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
            <polyline points="10 17 15 12 10 7" />
            <line x1="15" y1="12" x2="3" y2="12" />
          </svg>
        </div>
      </div>
      <h1 ref="titleRef" class="text-[28px] font-extrabold text-slate-800 tracking-tight leading-tight mt-4">
        Welcome back
      </h1>
      <p ref="subtitleRef" class="text-sm text-slate-500 mt-1.5 leading-relaxed">
        Sign in to your AthleteIQ account to continue your career journey.
      </p>
    </div>

    <!-- Social Login -->
    <div ref="socialRef">
      <button
        type="button"
        class="social-btn group"
        @click="handleSocialLogin('google')"
      >
        <svg class="w-[18px] h-[18px] shrink-0" viewBox="0 0 24 24">
          <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
          <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
          <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18A11.96 11.96 0 0 0 1 12c0 1.94.46 3.77 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
          <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
        </svg>
        <span class="text-sm font-semibold text-slate-700 group-hover:text-slate-900 transition-colors">Continue with Google</span>
      </button>
    </div>

    <!-- Divider -->
    <div ref="dividerRef" class="flex items-center gap-3">
      <div class="flex-1 h-px bg-gradient-to-r from-transparent via-slate-300 to-transparent"></div>
      <span class="text-[11px] font-medium text-slate-400 uppercase tracking-wider whitespace-nowrap">or sign in with email</span>
      <div class="flex-1 h-px bg-gradient-to-r from-transparent via-slate-300 to-transparent"></div>
    </div>

    <!-- Error Alert -->
    <BaseAlert v-if="error" type="error" :show="!!error" dismissible @dismiss="error = ''">
      {{ error }}
    </BaseAlert>

    <!-- Form -->
    <form ref="formRef" @submit.prevent="handleLogin" class="flex flex-col gap-4" novalidate>
      <div>
        <label for="login-email" class="flex items-center gap-1.5 text-[13px] font-semibold text-slate-600 mb-1.5">
          <svg viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5 text-slate-400">
            <path d="M3 4a2 2 0 0 0-2 2v1.161l8.441 4.221a1.25 1.25 0 0 0 1.118 0L19 7.162V6a2 2 0 0 0-2-2H3z"/>
            <path d="m19 8.839-7.77 3.885a2.75 2.75 0 0 1-2.46 0L1 8.839V14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8.839z"/>
          </svg>
          Email address
        </label>
        <BaseInput
          v-model="form.email"
          inputId="login-email"
          type="email"
          placeholder="you@example.com"
          autocomplete="email"
          :error="errors.email"
          required
          @blur="validateField('email')"
        />
      </div>

      <div>
        <div class="flex items-center justify-between mb-1.5">
          <label for="login-password" class="flex items-center gap-1.5 text-[13px] font-semibold text-slate-600">
            <svg viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5 text-slate-400">
              <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 0 0-4.5 4.5V9H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-.5V5.5A4.5 4.5 0 0 0 10 1zm3 8V5.5a3 3 0 1 0-6 0V9h6z" clip-rule="evenodd"/>
            </svg>
            Password
          </label>
          <button type="button" class="text-[11px] text-primary-600 font-semibold hover:text-primary-700 transition-colors" tabindex="-1">
            Forgot password?
          </button>
        </div>
        <div class="relative">
          <BaseInput
            v-model="form.password"
            inputId="login-password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Enter your password"
            autocomplete="current-password"
            :error="errors.password"
            required
            @blur="validateField('password')"
          />
          <button
            type="button"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors p-1 z-10"
            :aria-label="showPassword ? 'Hide password' : 'Show password'"
            @click="showPassword = !showPassword"
          >
            <svg v-if="showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
              <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Remember me -->
      <label class="flex items-center gap-2.5 cursor-pointer select-none group">
        <div class="relative w-[18px] h-[18px] shrink-0">
          <input v-model="rememberMe" type="checkbox" class="absolute inset-0 opacity-0 cursor-pointer z-10" />
          <div
            class="w-[18px] h-[18px] rounded-[5px] border-[1.5px] flex items-center justify-center transition-all duration-200"
            :class="rememberMe
              ? 'bg-gradient-to-br from-primary-600 to-primary-500 border-primary-600 shadow-sm shadow-primary-500/30'
              : 'bg-white border-slate-300'"
          >
            <svg v-if="rememberMe" viewBox="0 0 12 12" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-2.5 h-2.5">
              <polyline points="2.5 6 5 8.5 9.5 3.5"/>
            </svg>
          </div>
        </div>
        <span class="text-sm text-slate-600 group-hover:text-slate-800 transition-colors">Remember me for 30 days</span>
      </label>

      <!-- Submit -->
      <button
        ref="submitRef"
        type="submit"
        :disabled="loading"
        class="mt-1 w-full inline-flex items-center justify-center gap-2 font-semibold rounded-xl text-[15px] px-6 py-3 text-white transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-primary-500 disabled:opacity-60 disabled:cursor-not-allowed"
        :class="loading
          ? 'bg-primary-600'
          : 'bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-700 hover:to-primary-600 hover:-translate-y-0.5 active:translate-y-0 shadow-lg shadow-primary-500/25 hover:shadow-xl hover:shadow-primary-500/30'"
      >
        <AppSpinner v-if="loading" size="sm" color="white" />
        <svg v-else viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4">
          <path fill-rule="evenodd" d="M3 4.25A2.25 2.25 0 0 1 5.25 2h5.5A2.25 2.25 0 0 1 13 4.25v2a.75.75 0 0 1-1.5 0v-2a.75.75 0 0 0-.75-.75h-5.5a.75.75 0 0 0-.75.75v11.5c0 .414.336.75.75.75h5.5a.75.75 0 0 0 .75-.75v-2a.75.75 0 0 1 1.5 0v2A2.25 2.25 0 0 1 10.75 18h-5.5A2.25 2.25 0 0 1 3 15.75V4.25z" clip-rule="evenodd"/>
          <path fill-rule="evenodd" d="M19 10a.75.75 0 0 0-.75-.75H8.704l1.048-.943a.75.75 0 1 0-1.004-1.114l-2.5 2.25a.75.75 0 0 0 0 1.114l2.5 2.25a.75.75 0 1 0 1.004-1.114l-1.048-.943h9.546A.75.75 0 0 0 19 10z" clip-rule="evenodd"/>
        </svg>
        Sign in
      </button>
    </form>

    <!-- Footer -->
    <div ref="footerRef" class="mt-auto pt-3 border-t border-slate-200/60">
      <p class="text-center text-sm text-slate-500">
        Don't have an account?
        <router-link to="/auth/register" class="font-semibold text-primary-600 hover:text-primary-700 hover:underline hover:underline-offset-2 transition-colors">
          Create one →
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { isEmail, required } from '@/utils/validators'
import BaseInput from '@/components/BaseInput.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import AppSpinner from '@/components/AppSpinner.vue'
import { gsap } from 'gsap'

const { login } = useAuth()
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)

const form = reactive({ email: '', password: '' })
const errors = reactive({ email: '', password: '' })

// Template refs for GSAP
const pageRef = ref<HTMLElement | null>(null)
const iconRef = ref<HTMLElement | null>(null)
const titleRef = ref<HTMLElement | null>(null)
const subtitleRef = ref<HTMLElement | null>(null)
const socialRef = ref<HTMLElement | null>(null)
const dividerRef = ref<HTMLElement | null>(null)
const formRef = ref<HTMLElement | null>(null)
const submitRef = ref<HTMLElement | null>(null)
const footerRef = ref<HTMLElement | null>(null)

function validateField(field: 'email' | 'password') {
  if (field === 'email') {
    if (!required(form.email)) errors.email = 'Email is required'
    else if (!isEmail(form.email)) errors.email = 'Enter a valid email'
    else errors.email = ''
  }
  if (field === 'password') {
    errors.password = required(form.password) ? '' : 'Password is required'
  }
}

function validateAll(): boolean {
  validateField('email')
  validateField('password')
  return !errors.email && !errors.password
}

async function handleLogin() {
  if (!validateAll()) return
  loading.value = true
  error.value = ''
  try {
    await login(form)
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { message?: string } } }
    error.value = axiosErr.response?.data?.message ?? 'Invalid email or password'
  } finally {
    loading.value = false
  }
}

function handleSocialLogin(_provider: string) {
  // Social login placeholder – UI only
}

// Entrance animation using template refs
onMounted(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  const targets = [iconRef, titleRef, subtitleRef, socialRef, dividerRef, formRef, submitRef, footerRef]
  targets.forEach(t => {
    if (t.value) gsap.set(t.value, { opacity: 0, y: 16 })
  })

  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })

  if (iconRef.value) tl.to(iconRef.value, { opacity: 1, y: 0, scale: 1, duration: 0.45, delay: 0.1 })
  if (titleRef.value) tl.to(titleRef.value, { opacity: 1, y: 0, duration: 0.4 }, '-=0.2')
  if (subtitleRef.value) tl.to(subtitleRef.value, { opacity: 1, y: 0, duration: 0.35 }, '-=0.2')
  if (socialRef.value) tl.to(socialRef.value, { opacity: 1, y: 0, duration: 0.35 }, '-=0.15')
  if (dividerRef.value) tl.to(dividerRef.value, { opacity: 1, y: 0, duration: 0.3 }, '-=0.1')
  if (formRef.value) tl.to(formRef.value, { opacity: 1, y: 0, duration: 0.4 }, '-=0.1')
  if (submitRef.value) tl.to(submitRef.value, { opacity: 1, y: 0, duration: 0.35 }, '-=0.15')
  if (footerRef.value) tl.to(footerRef.value, { opacity: 1, y: 0, duration: 0.3 }, '-=0.1')
})
</script>

<style scoped>
/* Icon container */
.auth-icon-wrap {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.auth-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  z-index: 1;
  box-shadow: 0 4px 16px rgba(249, 115, 22, 0.25);
}

.auth-icon-glow {
  position: absolute;
  inset: -6px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.15), rgba(251, 146, 60, 0.08));
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.04); }
}

/* Social button */
.social-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 11px 16px;
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.social-btn:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transform: translateY(-1px);
}

.social-btn:active {
  transform: translateY(0);
}

/* Hide BaseInput's built-in label since we have custom ones */
:deep(.flex.flex-col.gap-1\.5 > label) {
  display: none;
}
</style>
