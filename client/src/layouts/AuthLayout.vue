<template>
  <div class="min-h-screen flex">
    <!-- Form panel -->
    <div class="w-full max-w-xl px-12 py-10 flex flex-col bg-white shadow-2xl z-10">
      <div class="flex items-center gap-3 mb-12">
        <span class="text-primary-600 flex">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-7 h-7">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
        </span>
        <span class="text-xl font-bold text-slate-800 tracking-tight">AthleteIQ</span>
      </div>
      <router-view v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </router-view>
    </div>

    <!-- Graphic panel -->
    <div class="hidden lg:flex flex-1 bg-gradient-to-br from-primary-950 via-primary-800 to-primary-600 items-center justify-center p-12">
      <div class="max-w-md text-indigo-100">
        <h2 class="text-4xl font-bold text-white leading-tight mb-4">
          Track, analyze,<br />and improve your<br />performance.
        </h2>
        <p class="text-base opacity-75 mb-12">
          Join thousands of athletes who use AthleteIQ to reach their goals.
        </p>
        <div class="flex gap-10">
          <div class="flex flex-col gap-1">
            <span class="text-2xl font-bold text-white">10k+</span>
            <span class="text-sm opacity-70">Athletes</span>
          </div>
          <div class="flex flex-col gap-1">
            <span class="text-2xl font-bold text-white">500k+</span>
            <span class="text-sm opacity-70">Workouts logged</span>
          </div>
          <div class="flex flex-col gap-1">
            <span class="text-2xl font-bold text-white">98%</span>
            <span class="text-sm opacity-70">Satisfaction</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
