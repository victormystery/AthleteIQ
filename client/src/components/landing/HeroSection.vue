<template>
  <section class="relative flex items-center pt-24 xs:pt-28 pb-28 lg:pb-20 lg:min-h-screen px-4 sm:px-6 overflow-hidden">
    <!-- Background gradient -->
    <div class="absolute inset-0 -z-10">
      <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-orange-50 via-white to-amber-50" />
      <div class="absolute top-0 right-0 w-[600px] h-[600px] bg-primary-100/50 rounded-full blur-3xl -translate-y-1/4 translate-x-1/4" />
      <div class="absolute bottom-0 left-0 w-[400px] h-[400px] bg-amber-100/40 rounded-full blur-3xl translate-y-1/4 -translate-x-1/4" />
    </div>

    <div class="max-w-6xl mx-auto w-full grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">

      <!-- Left: copy -->
      <div>
        <!-- Eyebrow badge -->
        <div class="mb-5 sm:mb-6 inline-flex items-center gap-2 bg-primary-50 border border-primary-200 text-primary-700 text-xs font-semibold px-4 py-1.5 rounded-full">
          <span class="w-1.5 h-1.5 rounded-full bg-primary-500 animate-pulse" />
          AI-Powered Career Guidance for Athletes
        </div>

        <!-- Headline -->
        <h1 class="text-4xl xs:text-5xl sm:text-6xl font-black tracking-tight text-slate-900 leading-[1.05]">
          Turn your athletic
          <span class="relative inline-block">
            <span class="relative z-10 text-primary-600">journey</span>
            <span class="absolute -bottom-1 left-0 w-full h-3 bg-primary-100 rounded-full -z-0" />
          </span>
          <br />into a career
        </h1>

        <p class="mt-5 sm:mt-6 text-base sm:text-lg text-slate-500 max-w-lg leading-relaxed">
          AthleteIQ uses machine learning to map your sports background, skills, and goals
          to the career pathways where athletes like you succeed.
        </p>

        <!-- CTAs -->
        <div class="mt-8 sm:mt-9 flex flex-col sm:flex-row items-stretch sm:items-start gap-3">
          <router-link
            to="/auth/register"
            class="group inline-flex items-center justify-center gap-2 px-7 py-3.5 text-base font-semibold text-white bg-primary-600 hover:bg-primary-700 rounded-2xl shadow-lg shadow-primary-200 transition-all duration-200 no-underline hover:-translate-y-0.5"
          >
            Start your assessment
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-4 h-4 transition-transform group-hover:translate-x-0.5">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </router-link>
          <a
            href="#how-it-works"
            class="inline-flex items-center justify-center gap-2 px-7 py-3.5 text-base font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 rounded-2xl transition-all duration-200 no-underline hover:-translate-y-0.5 shadow-sm"
            @click.prevent="scrollToSection('#how-it-works')"
          >
            See how it works
          </a>
        </div>

        <!-- Stats strip -->
        <div class="mt-8 sm:mt-12 flex items-center gap-4 sm:gap-8">
          <div v-for="(stat, i) in stats" :key="stat.label" class="flex items-center gap-3">
            <div v-if="i > 0" class="w-px h-8 bg-slate-200" />
            <div>
              <p class="text-xl sm:text-2xl font-black text-slate-900">{{ stat.value }}</p>
              <p class="text-[11px] sm:text-xs text-slate-500">{{ stat.label }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: dashboard preview mockup -->
      <div class="relative w-full pb-6 lg:pb-0 mt-4 lg:mt-0">
        <!-- Glow behind mockup -->
        <div class="absolute inset-0 bg-gradient-to-br from-primary-300/30 to-amber-300/20 rounded-3xl blur-2xl scale-95" />

        <!-- Browser chrome frame -->
        <div class="relative bg-white rounded-3xl shadow-2xl shadow-slate-300/50 border border-slate-200 overflow-hidden">
          <!-- Browser bar -->
          <div class="flex items-center gap-2 px-4 py-3 bg-slate-100 border-b border-slate-200">
            <span class="w-3 h-3 rounded-full bg-red-400" />
            <span class="w-3 h-3 rounded-full bg-amber-400" />
            <span class="w-3 h-3 rounded-full bg-green-400" />
            <div class="flex-1 mx-4 bg-white border border-slate-200 rounded-lg px-3 py-1 text-xs text-slate-400 font-medium truncate">
              athleteiq.app/dashboard
            </div>
          </div>

          <!-- Dashboard content -->
          <div class="flex h-[300px] sm:h-[400px]">
            <!-- Mini sidebar — hidden on small screens -->
            <div class="hidden sm:flex w-36 lg:w-40 bg-slate-900 flex-col shrink-0 p-3 gap-1">
              <div class="flex items-center gap-2 px-2 py-3 mb-2">
                <span class="w-5 h-5 rounded-md bg-primary-500 flex items-center justify-center">
                  <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" class="w-3 h-3">
                    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                  </svg>
                </span>
                <span class="text-xs font-bold text-white">AthleteIQ</span>
              </div>
              <div
                v-for="item in sidebarItems"
                :key="item.label"
                class="flex items-center gap-2 px-2 py-2 rounded-lg text-xs font-medium transition-colors"
                :class="item.active ? 'bg-primary-500/20 text-primary-400' : 'text-slate-500 hover:text-slate-300'"
              >
                <span v-html="item.icon" class="w-3.5 h-3.5 shrink-0" />
                {{ item.label }}
              </div>
            </div>

            <!-- Main dashboard area -->
            <div class="flex-1 bg-slate-50 p-3 sm:p-4 overflow-hidden">
              <!-- Welcome bar -->
              <div class="mb-3 sm:mb-4">
                <p class="text-xs font-bold text-slate-800">Your Career Recommendations</p>
                <p class="text-[10px] text-slate-400">Based on your athletic profile · 3 top matches</p>
              </div>

              <!-- Recommendation cards -->
              <div class="space-y-2 sm:space-y-2.5">
                <div
                  v-for="rec in dashboardRecs"
                  :key="rec.title"
                  class="bg-white rounded-xl p-2.5 sm:p-3 border flex items-center gap-2 sm:gap-3 shadow-sm"
                  :class="rec.featured ? 'border-primary-200 ring-1 ring-primary-100' : 'border-slate-200'"
                >
                  <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl flex items-center justify-center text-sm sm:text-base shrink-0" :class="rec.bg">
                    {{ rec.emoji }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between gap-2">
                      <p class="text-[11px] font-bold text-slate-800 truncate">{{ rec.title }}</p>
                      <span
                        class="text-[10px] font-bold shrink-0"
                        :class="rec.featured ? 'text-primary-600' : 'text-slate-400'"
                      >
                        {{ rec.score }}%
                      </span>
                    </div>
                    <!-- Confidence bar -->
                    <div class="mt-1.5 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        class="h-full rounded-full transition-all"
                        :class="rec.featured ? 'bg-primary-500' : 'bg-slate-300'"
                        :style="{ width: rec.score + '%' }"
                      />
                    </div>
                  </div>
                  <div v-if="rec.featured" class="shrink-0">
                    <span class="text-[9px] font-bold bg-primary-50 text-primary-600 border border-primary-200 px-2 py-0.5 rounded-full">
                      Top match
                    </span>
                  </div>
                </div>
              </div>

              <!-- Roadmap progress teaser -->
              <div class="mt-2.5 sm:mt-3 bg-white rounded-xl p-2.5 sm:p-3 border border-slate-200 flex items-center justify-between">
                <div>
                  <p class="text-[10px] font-bold text-slate-700">Roadmap progress</p>
                  <p class="text-[9px] text-slate-400">Sports Analytics · Milestone 2 of 6</p>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-14 sm:w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full w-[33%] bg-primary-500 rounded-full" />
                  </div>
                  <span class="text-[10px] font-bold text-primary-600">33%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Floating badge -->
        <div class="absolute -bottom-4 left-4 sm:-left-4 bg-white rounded-2xl shadow-xl border border-slate-200 px-3 sm:px-4 py-2.5 sm:py-3 flex items-center gap-2 sm:gap-3">
          <span class="w-7 h-7 sm:w-8 sm:h-8 rounded-xl bg-green-100 flex items-center justify-center text-sm sm:text-base">✅</span>
          <div>
            <p class="text-xs font-bold text-slate-800">Assessment complete</p>
            <p class="text-[10px] text-slate-400">Results ready in seconds</p>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup lang="ts">
import { stats, sidebarItems, dashboardRecs } from '@/data/landingData'

function scrollToSection(href: string) {
  const el = document.querySelector(href)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>
