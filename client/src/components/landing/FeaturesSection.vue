<template>
  <section id="features" class="py-24 px-4 bg-slate-50">
    <div class="max-w-6xl mx-auto">
      <!-- Section header -->
      <div class="text-center mb-16">
        <p class="text-sm font-bold uppercase tracking-widest text-primary-600 mb-3">Features</p>
        <h2 class="text-4xl sm:text-5xl font-black text-slate-900 tracking-tight">
          Built for athletes, by design
        </h2>
        <p class="mt-4 text-lg text-slate-500 max-w-xl mx-auto">
          Every feature is crafted around the unique transition athletes face when moving beyond competition.
        </p>
      </div>

      <div class="grid md:grid-cols-3 gap-6">
        <div
          v-for="feature in features"
          :key="feature.title"
          class="group bg-white rounded-3xl p-8 border border-slate-200 hover:border-primary-200 hover:shadow-xl hover:shadow-primary-50 transition-all duration-300 hover:-translate-y-1"
        >
          <div
            class="w-12 h-12 rounded-2xl flex items-center justify-center mb-6 transition-colors duration-300"
            :class="feature.iconBg"
          >
            <span v-html="feature.icon" class="w-6 h-6" :class="feature.iconColor" />
          </div>
          <h3 class="text-xl font-bold text-slate-900 mb-3">{{ feature.title }}</h3>
          <p class="text-slate-500 leading-relaxed">{{ feature.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { features } from '@/data/landingData'
</script>
