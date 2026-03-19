<template>
  <section id="how-it-works" class="py-16 md:py-24 px-4 sm:px-6">
    <div class="max-w-5xl mx-auto">
      <div class="text-center mb-10 md:mb-16">
        <p class="text-sm font-bold uppercase tracking-widest text-primary-600 mb-3">Process</p>
        <h2 class="text-3xl xs:text-4xl sm:text-5xl font-black text-slate-900 tracking-tight">
          Your path in four steps
        </h2>
      </div>

      <!-- mt-4 gives headroom so the -top-3 step badge doesn't clip -->
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 sm:gap-6 mt-4">
        <div
          v-for="(step, i) in steps"
          :key="step.title"
          class="relative bg-white rounded-3xl p-5 sm:p-7 border border-slate-200 hover:border-primary-200 transition-all duration-200 hover:shadow-lg"
        >
          <!-- Step number -->
          <span class="absolute -top-3 -left-3 w-8 h-8 rounded-xl bg-primary-600 text-white text-sm font-black flex items-center justify-center shadow-md">
            {{ i + 1 }}
          </span>
          <div class="w-12 h-12 rounded-2xl flex items-center justify-center bg-gradient-to-br from-primary-100 to-amber-50 shadow-md shadow-primary-100/50 ring-1 ring-primary-200/40 mb-4 sm:mb-5">
            <span class="text-2xl leading-none select-none">{{ step.icon }}</span>
          </div>
          <h3 class="text-base font-bold text-slate-900 mb-2">{{ step.title }}</h3>
          <p class="text-sm text-slate-500 leading-relaxed">{{ step.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { steps } from '@/data/landingData'
</script>
