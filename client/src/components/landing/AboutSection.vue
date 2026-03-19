<template>
  <section id="about" class="py-16 md:py-24 px-4 sm:px-6">
    <div class="max-w-6xl mx-auto">
      <div class="grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">

        <!-- Left: copy + metrics -->
        <div>
          <p class="text-sm font-bold uppercase tracking-widest text-primary-600 mb-4">About AthleteIQ</p>
          <h2 class="text-3xl xs:text-4xl sm:text-5xl font-black text-slate-900 tracking-tight leading-[1.1]">
            We understand the athlete's career dilemma
          </h2>
          <p class="mt-5 sm:mt-6 text-base sm:text-lg text-slate-500 leading-relaxed">
            Most athletes spend years building sport-specific skills without a clear roadmap for what comes next.
            AthleteIQ bridges that gap with data-driven career matching powered by machine learning.
          </p>
          <p class="mt-4 text-base sm:text-lg text-slate-500 leading-relaxed">
            Our system analyses your sport, academic background, motivations, and work preferences to surface
            the career pathways where athletes with your profile thrive.
          </p>
          <div class="mt-7 sm:mt-8 grid grid-cols-2 gap-4 sm:gap-6">
            <div
              v-for="metric in metrics"
              :key="metric.label"
              class="bg-slate-50 rounded-2xl p-4 sm:p-5 border border-slate-200"
            >
              <p class="text-2xl sm:text-3xl font-black text-primary-600">{{ metric.value }}</p>
              <p class="text-xs sm:text-sm text-slate-500 mt-1">{{ metric.label }}</p>
            </div>
          </div>
        </div>

        <!-- Right: testimonials -->
        <div class="space-y-4">
          <div
            v-for="testimonial in testimonials"
            :key="testimonial.name"
            class="bg-white rounded-3xl p-5 sm:p-7 border border-slate-200 hover:border-slate-300 hover:shadow-lg transition-all duration-200"
          >
            <!-- Stars -->
            <div class="flex gap-0.5 mb-4">
              <svg v-for="n in 5" :key="n" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 text-amber-400">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
            </div>
            <p class="text-sm sm:text-base text-slate-700 leading-relaxed italic">"{{ testimonial.quote }}"</p>
            <div class="mt-4 sm:mt-5 flex items-center gap-3">
              <div class="w-9 h-9 rounded-xl bg-primary-100 flex items-center justify-center text-sm font-bold text-primary-700 shrink-0">
                {{ testimonial.name.charAt(0) }}
              </div>
              <div class="min-w-0">
                <p class="text-sm font-semibold text-slate-900 truncate">{{ testimonial.name }}</p>
                <p class="text-xs text-slate-400 truncate">{{ testimonial.role }}</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { metrics, testimonials } from '@/data/landingData'
</script>
