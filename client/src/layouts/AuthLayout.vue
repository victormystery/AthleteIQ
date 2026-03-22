<template>
  <div class="auth-layout min-h-screen flex flex-col lg:flex-row">
    <!-- Left branding panel (desktop only) -->
    <div class="branding-panel hidden lg:flex lg:w-[44%] xl:w-[40%] flex-col p-8 bg-white">
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-2.5 no-underline group">
        <span class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-5 h-5">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
        </span>
        <span class="text-xl font-bold text-slate-800 tracking-tight group-hover:text-primary-600 transition-colors">AthleteIQ</span>
      </router-link>

      <!-- Hero image area -->
      <div ref="heroRef" class="hero-visual flex-1 mt-8 rounded-2xl overflow-hidden relative min-h-72">
        <!-- Animated gradient background -->
        <div class="hero-gradient"></div>

        <!-- Decorative orbs -->
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>

        <!-- Subtle mesh pattern -->
        <div class="mesh-pattern"></div>

        <!-- Subtle sport graphic -->
        <div class="absolute top-8 right-8 opacity-[0.07]">
          <svg viewBox="0 0 96 96" fill="none" class="w-28 h-28 text-white">
            <circle cx="48" cy="48" r="44" stroke="currentColor" stroke-width="2"/>
            <circle cx="48" cy="48" r="30" stroke="currentColor" stroke-width="1.5"/>
            <circle cx="48" cy="48" r="16" stroke="currentColor" stroke-width="1.5"/>
            <path d="M4 48h88M48 4v88" stroke="currentColor" stroke-width="1.5"/>
          </svg>
        </div>

        <!-- Stats row -->
        <div ref="statsRef" class="absolute top-8 left-8 flex gap-8">
          <div v-for="stat in stats" :key="stat.label" class="stat-item">
            <p class="text-2xl font-bold text-white">{{ stat.value }}</p>
            <p class="text-xs text-primary-300 mt-0.5">{{ stat.label }}</p>
          </div>
        </div>

        <!-- Bottom overlay text -->
        <div class="absolute bottom-0 inset-x-0 p-8 bg-gradient-to-t from-primary-950/90 via-primary-950/40 to-transparent">
          <h2 ref="headlineRef" class="text-3xl font-bold text-white leading-snug">
            Begin Your<br/>Journey
          </h2>
          <p ref="subtitleRef" class="text-primary-200 text-sm mt-2 leading-relaxed opacity-90">
            Discover your next career path<br/>beyond the game.
          </p>
        </div>
      </div>

      <!-- Bottom tagline -->
      <div class="mt-6 flex items-center gap-2 text-slate-400 text-sm">
        <svg viewBox="0 0 16 16" fill="currentColor" class="w-3 h-3 text-primary-400 shrink-0">
          <path d="M8 0L9.8 5.6H16L11 9.1L12.8 14.7L8 11.2L3.2 14.7L5 9.1L0 5.6H6.2L8 0Z"/>
        </svg>
        <span>Cultivating champions, one step at a time.</span>
      </div>
    </div>

    <!-- Right form panel -->
    <div class="form-panel flex-1 bg-[#f5f0e8] flex flex-col min-h-screen lg:min-h-0">
      <!-- Mobile logo header -->
      <div class="flex lg:hidden items-center gap-2.5 px-6 py-5 bg-white border-b border-[#e8e1d8]">
        <router-link to="/" class="flex items-center gap-2.5 no-underline">
          <span class="logo-icon-sm">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-5 h-5">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
            </svg>
          </span>
          <span class="text-lg font-bold text-slate-800 tracking-tight">AthleteIQ</span>
        </router-link>
      </div>

      <!-- Form container -->
      <div class="flex-1 flex items-center justify-center px-6 py-10 sm:px-10">
        <div class="w-full max-w-md">
          <router-view v-slot="{ Component }">
            <Transition name="auth-slide" mode="out-in">
              <component :is="Component" />
            </Transition>
          </router-view>
        </div>
      </div>

      <!-- Security badge (mobile) -->
      <div class="flex lg:hidden items-center justify-center gap-2 pb-6 text-xs text-slate-400">
        <svg viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5">
          <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 0 0-4.5 4.5V9H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-.5V5.5A4.5 4.5 0 0 0 10 1zm3 8V5.5a3 3 0 1 0-6 0V9h6z" clip-rule="evenodd"/>
        </svg>
        <span>256-bit SSL encrypted</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'

const heroRef = ref<HTMLElement | null>(null)
const statsRef = ref<HTMLElement | null>(null)
const headlineRef = ref<HTMLElement | null>(null)
const subtitleRef = ref<HTMLElement | null>(null)

const stats = [
  { value: '10k+', label: 'Athletes' },
  { value: '98%', label: 'Satisfaction' },
  { value: '500k+', label: 'Careers matched' }
]

onMounted(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })

  tl.from(heroRef.value as Element, { opacity: 0, y: 30, duration: 0.8 })
    .from('.stat-item', { opacity: 0, y: 16, duration: 0.5, stagger: 0.1 }, '-=0.4')
    .from(headlineRef.value as Element, { opacity: 0, y: 20, duration: 0.5 }, '-=0.3')
    .from(subtitleRef.value as Element, { opacity: 0, y: 14, duration: 0.4 }, '-=0.25')

  // Floating orb animations
  gsap.to('.orb-1', { y: -20, x: 10, duration: 6, ease: 'sine.inOut', yoyo: true, repeat: -1 })
  gsap.to('.orb-2', { y: 15, x: -8, duration: 8, ease: 'sine.inOut', yoyo: true, repeat: -1 })
  gsap.to('.orb-3', { y: -12, x: 5, duration: 7, ease: 'sine.inOut', yoyo: true, repeat: -1 })
})
</script>

<style scoped>
/* Logo icon */
.logo-icon {
  width: 32px;
  height: 32px;
  border-radius: 9px;
  background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.2);
}

.logo-icon-sm {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.logo-icon-sm svg {
  width: 14px;
  height: 14px;
}

/* Hero visual */
.hero-visual {
  position: relative;
  isolation: isolate;
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #431407 0%, #7c2d12 25%, #9a3412 45%, #c2410c 70%, #ea580c 100%);
  z-index: -3;
}

/* Decorative orbs */
.orb {
  position: absolute;
  border-radius: 50%;
  z-index: -2;
}

.orb-1 {
  top: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
}

.orb-2 {
  top: 33%;
  left: -40px;
  width: 160px;
  height: 160px;
  background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
}

.orb-3 {
  bottom: -30px;
  right: 30px;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 70%);
}

/* Mesh pattern overlay */
.mesh-pattern {
  position: absolute;
  inset: 0;
  z-index: -1;
  opacity: 0.03;
  background-image:
    radial-gradient(circle at 25% 25%, white 1px, transparent 1px),
    radial-gradient(circle at 75% 75%, white 1px, transparent 1px);
  background-size: 28px 28px;
}

/* Stat item */
.stat-item {
  position: relative;
}

.stat-item + .stat-item::before {
  content: '';
  position: absolute;
  left: -16px;
  top: 4px;
  bottom: 4px;
  width: 1px;
  background: rgba(255, 255, 255, 0.15);
}

/* Auth transition */
.auth-slide-enter-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.auth-slide-leave-active {
  transition: all 0.2s ease;
}
.auth-slide-enter-from {
  opacity: 0;
  transform: translateX(24px);
}
.auth-slide-leave-to {
  opacity: 0;
  transform: translateX(-24px);
}

/* Form panel subtle texture */
.form-panel {
  background: #f5f0e8;
  background-image:
    radial-gradient(circle at 20% 80%, rgba(234, 88, 12, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(234, 88, 12, 0.02) 0%, transparent 50%);
}
</style>
