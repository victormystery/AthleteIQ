<template>
  <div class="bg-white text-slate-900 overflow-x-hidden">
    <AppHeader />

    <!-- ── Hero ──────────────────────────────────────────────────────── -->
    <section class="relative flex items-center pt-28 pb-20 lg:min-h-screen px-4 overflow-hidden">
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
          <div class="mb-6 inline-flex items-center gap-2 bg-primary-50 border border-primary-200 text-primary-700 text-xs font-semibold px-4 py-1.5 rounded-full">
            <span class="w-1.5 h-1.5 rounded-full bg-primary-500 animate-pulse" />
            AI-Powered Career Guidance for Athletes
          </div>

          <!-- Headline -->
          <h1 class="text-5xl sm:text-6xl font-black tracking-tight text-slate-900 leading-[1.05]">
            Turn your athletic
            <span class="relative inline-block">
              <span class="relative z-10 text-primary-600">journey</span>
              <span class="absolute -bottom-1 left-0 w-full h-3 bg-primary-100 rounded-full -z-0" />
            </span>
            <br />into a career
          </h1>

          <p class="mt-6 text-lg text-slate-500 max-w-lg leading-relaxed">
            AthleteIQ uses machine learning to map your sports background, skills, and goals
            to the career pathways where athletes like you succeed.
          </p>

          <!-- CTAs -->
          <div class="mt-9 flex flex-col sm:flex-row items-start gap-3">
            <router-link
              to="/auth/register"
              class="group inline-flex items-center gap-2 px-7 py-3.5 text-base font-semibold text-white bg-primary-600 hover:bg-primary-700 rounded-2xl shadow-lg shadow-primary-200 transition-all duration-200 no-underline hover:-translate-y-0.5"
            >
              Start your assessment
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-4 h-4 transition-transform group-hover:translate-x-0.5">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </router-link>
            <a
              href="#how-it-works"
              class="inline-flex items-center gap-2 px-7 py-3.5 text-base font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 rounded-2xl transition-all duration-200 no-underline hover:-translate-y-0.5 shadow-sm"
              @click.prevent="scrollTo('#how-it-works')"
            >
              See how it works
            </a>
          </div>

          <!-- Stats strip -->
          <div class="mt-12 flex items-center gap-8">
            <div v-for="(stat, i) in stats" :key="stat.label" class="flex items-center gap-3">
              <div v-if="i > 0" class="w-px h-8 bg-slate-200" />
              <div>
                <p class="text-2xl font-black text-slate-900">{{ stat.value }}</p>
                <p class="text-xs text-slate-500">{{ stat.label }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: dashboard preview mockup -->
        <div class="relative w-full">
          <!-- Glow behind mockup -->
          <div class="absolute inset-0 bg-gradient-to-br from-primary-300/30 to-amber-300/20 rounded-3xl blur-2xl scale-95" />

          <!-- Browser chrome frame -->
          <div class="relative bg-white rounded-3xl shadow-2xl shadow-slate-300/50 border border-slate-200 overflow-hidden">
            <!-- Browser bar -->
            <div class="flex items-center gap-2 px-4 py-3 bg-slate-100 border-b border-slate-200">
              <span class="w-3 h-3 rounded-full bg-red-400" />
              <span class="w-3 h-3 rounded-full bg-amber-400" />
              <span class="w-3 h-3 rounded-full bg-green-400" />
              <div class="flex-1 mx-4 bg-white border border-slate-200 rounded-lg px-3 py-1 text-xs text-slate-400 font-medium">
                athleteiq.app/dashboard
              </div>
            </div>

            <!-- Dashboard content -->
            <div class="flex h-[320px] sm:h-[400px]">
              <!-- Mini sidebar — hidden on very small screens to save space -->
              <div class="hidden sm:flex w-36 lg:w-40 bg-slate-900 flex-col shrink-0 p-3 gap-1">
                <div class="flex items-center gap-2 px-2 py-3 mb-2">
                  <span class="w-5 h-5 rounded-md bg-primary-500 flex items-center justify-center">
                    <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" class="w-3 h-3">
                      <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                    </svg>
                  </span>
                  <span class="text-xs font-bold text-white">AthleteIQ</span>
                </div>
                <div v-for="item in sidebarItems" :key="item.label"
                  class="flex items-center gap-2 px-2 py-2 rounded-lg text-xs font-medium transition-colors"
                  :class="item.active ? 'bg-primary-500/20 text-primary-400' : 'text-slate-500 hover:text-slate-300'"
                >
                  <span v-html="item.icon" class="w-3.5 h-3.5 shrink-0" />
                  {{ item.label }}
                </div>
              </div>

              <!-- Main dashboard area -->
              <div class="flex-1 bg-slate-50 p-4 overflow-hidden">
                <!-- Welcome bar -->
                <div class="mb-4">
                  <p class="text-xs font-bold text-slate-800">Your Career Recommendations</p>
                  <p class="text-[10px] text-slate-400">Based on your athletic profile · 3 top matches</p>
                </div>

                <!-- Recommendation cards -->
                <div class="space-y-2.5">
                  <div v-for="rec in dashboardRecs" :key="rec.title"
                    class="bg-white rounded-xl p-3 border flex items-center gap-3 shadow-sm"
                    :class="rec.featured ? 'border-primary-200 ring-1 ring-primary-100' : 'border-slate-200'"
                  >
                    <div class="w-9 h-9 rounded-xl flex items-center justify-center text-base shrink-0"
                      :class="rec.bg">
                      {{ rec.emoji }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center justify-between gap-2">
                        <p class="text-[11px] font-bold text-slate-800 truncate">{{ rec.title }}</p>
                        <span class="text-[10px] font-bold shrink-0"
                          :class="rec.featured ? 'text-primary-600' : 'text-slate-400'">
                          {{ rec.score }}%
                        </span>
                      </div>
                      <!-- Confidence bar -->
                      <div class="mt-1.5 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div class="h-full rounded-full transition-all"
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

                <!-- Bottom progress teaser -->
                <div class="mt-3 bg-white rounded-xl p-3 border border-slate-200 flex items-center justify-between">
                  <div>
                    <p class="text-[10px] font-bold text-slate-700">Roadmap progress</p>
                    <p class="text-[9px] text-slate-400">Sports Analytics · Milestone 2 of 6</p>
                  </div>
                  <div class="flex items-center gap-2">
                    <div class="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div class="h-full w-[33%] bg-primary-500 rounded-full" />
                    </div>
                    <span class="text-[10px] font-bold text-primary-600">33%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Floating badge -->
          <div class="absolute -bottom-4 left-4 sm:-left-4 bg-white rounded-2xl shadow-xl border border-slate-200 px-4 py-3 flex items-center gap-3">
            <span class="w-8 h-8 rounded-xl bg-green-100 flex items-center justify-center text-base">✅</span>
            <div>
              <p class="text-xs font-bold text-slate-800">Assessment complete</p>
              <p class="text-[10px] text-slate-400">Results ready in seconds</p>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ── Features ───────────────────────────────────────────────────── -->
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
            <div class="w-12 h-12 rounded-2xl flex items-center justify-center mb-6 transition-colors duration-300"
              :class="feature.iconBg">
              <span v-html="feature.icon" class="w-6 h-6" :class="feature.iconColor" />
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">{{ feature.title }}</h3>
            <p class="text-slate-500 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── How it works ───────────────────────────────────────────────── -->
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

    <!-- ── Career Pathways ────────────────────────────────────────────── -->
    <section id="pathways" class="py-24 px-4 bg-slate-50">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-16">
          <p class="text-sm font-bold uppercase tracking-widest text-primary-600 mb-3">Pathways</p>
          <h2 class="text-4xl sm:text-5xl font-black text-slate-900 tracking-tight">
            11 career pathways explored
          </h2>
          <p class="mt-4 text-lg text-slate-500 max-w-xl mx-auto">
            From coaching to sports law, we map every route from the field to a fulfilling career.
          </p>
        </div>

        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <div
            v-for="pathway in pathways"
            :key="pathway.title"
            class="group bg-white rounded-3xl p-6 border border-slate-200 hover:border-primary-300 hover:shadow-lg hover:shadow-slate-100 transition-all duration-300 cursor-pointer"
          >
            <div class="flex items-center gap-4 mb-4">
              <div class="w-11 h-11 rounded-2xl flex items-center justify-center text-xl shrink-0"
                :class="pathway.bg">
                {{ pathway.emoji }}
              </div>
              <div>
                <h3 class="text-sm font-bold text-slate-900">{{ pathway.title }}</h3>
                <p class="text-xs text-slate-400">{{ pathway.salary }}</p>
              </div>
            </div>
            <p class="text-sm text-slate-500 leading-relaxed">{{ pathway.description }}</p>
            <div class="mt-4 flex flex-wrap gap-1.5">
              <span
                v-for="tag in pathway.tags"
                :key="tag"
                class="text-xs font-medium px-2.5 py-1 rounded-full bg-slate-100 text-slate-600"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </div>

        <div class="text-center mt-10">
          <router-link
            to="/auth/register"
            class="inline-flex items-center gap-2 px-6 py-3 text-sm font-semibold text-primary-700 bg-primary-50 hover:bg-primary-100 border border-primary-200 rounded-2xl transition-all no-underline"
          >
            View all 11 pathways
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-4 h-4">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ── Social proof / About ───────────────────────────────────────── -->
    <section id="about" class="py-24 px-4">
      <div class="max-w-6xl mx-auto">
        <div class="grid lg:grid-cols-2 gap-16 items-center">
          <!-- Left copy -->
          <div>
            <p class="text-sm font-bold uppercase tracking-widest text-primary-600 mb-4">About AthleteIQ</p>
            <h2 class="text-4xl sm:text-5xl font-black text-slate-900 tracking-tight leading-[1.1]">
              We understand the athlete's career dilemma
            </h2>
            <p class="mt-6 text-lg text-slate-500 leading-relaxed">
              Most athletes spend years building sport-specific skills without a clear roadmap for what comes next.
              AthleteIQ bridges that gap with data-driven career matching powered by machine learning.
            </p>
            <p class="mt-4 text-lg text-slate-500 leading-relaxed">
              Our system analyses your sport, academic background, motivations, and work preferences to surface
              the career pathways where athletes with your profile thrive.
            </p>
            <div class="mt-8 grid grid-cols-2 gap-6">
              <div v-for="metric in metrics" :key="metric.label" class="bg-slate-50 rounded-2xl p-5 border border-slate-200">
                <p class="text-3xl font-black text-primary-600">{{ metric.value }}</p>
                <p class="text-sm text-slate-500 mt-1">{{ metric.label }}</p>
              </div>
            </div>
          </div>

          <!-- Right: testimonial cards -->
          <div class="space-y-4">
            <div
              v-for="testimonial in testimonials"
              :key="testimonial.name"
              class="bg-white rounded-3xl p-7 border border-slate-200 hover:border-slate-300 hover:shadow-lg transition-all duration-200"
            >
              <!-- Stars -->
              <div class="flex gap-0.5 mb-4">
                <svg v-for="n in 5" :key="n" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4 text-amber-400">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
              <p class="text-slate-700 leading-relaxed italic">"{{ testimonial.quote }}"</p>
              <div class="mt-5 flex items-center gap-3">
                <div class="w-9 h-9 rounded-xl bg-primary-100 flex items-center justify-center text-sm font-bold text-primary-700">
                  {{ testimonial.name.charAt(0) }}
                </div>
                <div>
                  <p class="text-sm font-semibold text-slate-900">{{ testimonial.name }}</p>
                  <p class="text-xs text-slate-400">{{ testimonial.role }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA Banner ─────────────────────────────────────────────────── -->
    <section class="py-20 px-4">
      <div class="max-w-5xl mx-auto">
        <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-600 to-primary-800 px-8 py-16 text-center shadow-2xl shadow-primary-200">
          <!-- Decorative circles -->
          <div class="absolute -top-16 -right-16 w-64 h-64 bg-white/10 rounded-full" />
          <div class="absolute -bottom-12 -left-12 w-48 h-48 bg-white/10 rounded-full" />

          <div class="relative z-10">
            <h2 class="text-4xl sm:text-5xl font-black text-white tracking-tight">
              Ready to find your path?
            </h2>
            <p class="mt-4 text-lg text-primary-200 max-w-xl mx-auto">
              Complete the 5-minute assessment and get personalised career recommendations instantly.
            </p>
            <div class="mt-10 flex flex-col sm:flex-row items-center justify-center gap-3">
              <router-link
                to="/auth/register"
                class="inline-flex items-center gap-2 px-7 py-3.5 text-base font-semibold text-primary-700 bg-white hover:bg-primary-50 rounded-2xl transition-all no-underline shadow-lg"
              >
                Create free account
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-4 h-4">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </router-link>
              <router-link
                to="/auth/login"
                class="inline-flex items-center gap-2 px-7 py-3.5 text-base font-semibold text-white/80 hover:text-white border border-white/30 hover:border-white/60 rounded-2xl transition-all no-underline"
              >
                Already have an account
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Footer ─────────────────────────────────────────────────────── -->
    <footer class="border-t border-slate-200 py-12 px-4">
      <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-6">
        <div class="flex items-center gap-2.5">
          <span class="flex items-center justify-center w-7 h-7 rounded-lg bg-primary-600 text-white">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-3.5 h-3.5">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
            </svg>
          </span>
          <span class="text-sm font-bold text-slate-800">AthleteIQ</span>
        </div>
        <p class="text-sm text-slate-400">
          &copy; {{ new Date().getFullYear() }} AthleteIQ. Empowering athlete career transitions.
        </p>
        <div class="flex items-center gap-5">
          <router-link to="/auth/login" class="text-sm text-slate-500 hover:text-slate-800 no-underline">Login</router-link>
          <router-link to="/auth/register" class="text-sm text-slate-500 hover:text-slate-800 no-underline">Register</router-link>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'

function scrollTo(href: string) {
  const el = document.querySelector(href)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

const sidebarItems = [
  {
    label: 'Dashboard',
    active: true,
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>'
  },
  {
    label: 'Pathways',
    active: false,
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>'
  },
  {
    label: 'Roadmap',
    active: false,
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
  },
  {
    label: 'Profile',
    active: false,
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
  }
]

const dashboardRecs = [
  { emoji: '📊', title: 'Sports Analytics', score: 91, featured: true, bg: 'bg-primary-50' },
  { emoji: '🏋️', title: 'High Performance Sport', score: 78, featured: false, bg: 'bg-amber-50' },
  { emoji: '🧬', title: 'Sports Science & Medicine', score: 65, featured: false, bg: 'bg-red-50' }
]

const stats = [
  { value: '11', label: 'Career pathways' },
  { value: '14', label: 'Assessed dimensions' },
  { value: '95%', label: 'Satisfaction rate' }
]

const features = [
  {
    title: 'AI-Powered Matching',
    description: 'Our ML model analyses 14 dimensions of your athletic profile to surface the career pathways where you are most likely to succeed.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>',
    iconBg: 'bg-primary-50',
    iconColor: 'text-primary-600'
  },
  {
    title: 'Personalised Roadmaps',
    description: 'Get step-by-step milestone roadmaps with certifications, estimated costs, and curated resources for each recommended pathway.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>',
    iconBg: 'bg-emerald-50',
    iconColor: 'text-emerald-600'
  },
  {
    title: 'Progress Tracking',
    description: 'Track your journey through each milestone, update your status, and see your overall progress percentage as you advance.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8v8m-8-5v5M8 3v1m8-1v1M3 9h1m16 0h1m-3.5-4.5l-.707.707M6.207 5.207l-.707-.707M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
    iconBg: 'bg-amber-50',
    iconColor: 'text-amber-600'
  }
]

const steps = [
  {
    title: 'Create your account',
    description: 'Sign up in under a minute with just your name, email, and sport.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>'
  },
  {
    title: 'Complete the questionnaire',
    description: 'Answer 14 questions covering your sport, academics, leadership, and career motivation.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>'
  },
  {
    title: 'Get your recommendations',
    description: 'Our ML model processes your profile and returns ranked career pathways with confidence scores.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>'
  },
  {
    title: 'Follow your roadmap',
    description: 'Access detailed milestone roadmaps, resources, and track your progress toward your new career.',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
  }
]

const pathways = [
  {
    emoji: '🏋️',
    title: 'High Performance Sport',
    salary: '$55k – $120k',
    description: 'Coaching, performance analysis, and athlete development roles within elite programs.',
    tags: ['Coaching', 'Analysis', 'Leadership'],
    bg: 'bg-amber-50'
  },
  {
    emoji: '📊',
    title: 'Sports Analytics',
    salary: '$65k – $130k',
    description: 'Data-driven roles using statistics and ML to optimise team and athlete performance.',
    tags: ['Data', 'Python', 'Statistics'],
    bg: 'bg-amber-50'
  },
  {
    emoji: '🏢',
    title: 'Sports Management',
    salary: '$50k – $100k',
    description: 'Operations, events, sponsorship, and commercial roles within sports organisations.',
    tags: ['Operations', 'Business', 'Events'],
    bg: 'bg-green-50'
  },
  {
    emoji: '🧬',
    title: 'Sports Science & Medicine',
    salary: '$60k – $115k',
    description: 'Exercise physiology, biomechanics, physiotherapy, and sports nutrition research.',
    tags: ['Physiology', 'Research', 'Medicine'],
    bg: 'bg-red-50'
  },
  {
    emoji: '📺',
    title: 'Sports Media & Journalism',
    salary: '$45k – $90k',
    description: 'Broadcasting, writing, podcasting, and content creation for sports audiences.',
    tags: ['Media', 'Writing', 'Content'],
    bg: 'bg-purple-50'
  },
  {
    emoji: '⚖️',
    title: 'Sports Law & Ethics',
    salary: '$70k – $150k',
    description: 'Contract negotiation, regulatory compliance, and athlete rights representation.',
    tags: ['Law', 'Compliance', 'Contracts'],
    bg: 'bg-slate-100'
  }
]

const metrics = [
  { value: '11', label: 'Career pathways mapped' },
  { value: '14', label: 'Profile dimensions' },
  { value: '6', label: 'Milestones per pathway' },
  { value: '3', label: 'User roles supported' }
]

const testimonials = [
  {
    quote: 'The questionnaire identified sports analytics as my top match. Two years later, I\'m a performance analyst for a professional rugby club.',
    name: 'James Okonkwo',
    role: 'Former sprinter → Performance Analyst'
  },
  {
    quote: 'I had no idea my captaincy experience translated so directly to sports management. AthleteIQ showed me the connection.',
    name: 'Sarah Mitchell',
    role: 'Former swimmer → Sports Manager'
  }
]
</script>
