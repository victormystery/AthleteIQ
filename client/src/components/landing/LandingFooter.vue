<template>
  <footer class="border-t border-slate-200 py-8 sm:py-12 px-4 sm:px-6">
    <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 sm:gap-6">
      <!-- Brand -->
      <div class="flex items-center gap-2.5">
        <span class="flex items-center justify-center w-7 h-7 rounded-lg bg-primary-600 text-white">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-3.5 h-3.5">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
        </span>
        <span class="text-sm font-bold text-slate-800">AthleteIQ</span>
      </div>

      <p class="text-sm text-slate-400 text-center">
        &copy; {{ currentYear }} AthleteIQ. Empowering athlete career transitions.
      </p>

      <!-- Links -->
      <div class="flex items-center gap-5">
        <router-link to="/auth/login" class="text-sm text-slate-500 hover:text-slate-800 no-underline py-1">Login</router-link>
        <router-link to="/auth/register" class="text-sm text-slate-500 hover:text-slate-800 no-underline py-1">Register</router-link>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>
