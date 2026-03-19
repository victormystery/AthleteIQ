<template>
  <section id="how-it-works" class="py-24 px-4">
    <div class="max-w-5xl mx-auto">
      <div class="text-center mb-16">
        <p class="text-sm font-bold uppercase tracking-widest text-primary-600 mb-3">Process</p>
        <h2 class="text-4xl sm:text-5xl font-black text-slate-900 tracking-tight">
          Your path in four steps
        </h2>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="(step, i) in steps"
          :key="step.title"
          class="relative bg-white rounded-3xl p-7 border border-slate-200 hover:border-primary-200 transition-all duration-200 hover:shadow-lg"
        >
          <!-- Step number -->
          <span class="absolute -top-3 -left-3 w-8 h-8 rounded-xl bg-primary-600 text-white text-sm font-black flex items-center justify-center shadow-md">
            {{ i + 1 }}
          </span>
          <div class="w-10 h-10 rounded-xl flex items-center justify-center bg-primary-50 mb-5">
            <span v-html="step.icon" class="w-5 h-5 text-primary-600" />
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
