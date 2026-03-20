<template>
  <header
    class="fixed top-0 inset-x-0 z-50 transition-all duration-300"
    :class="scrolled ? 'py-3' : 'py-5'"
  >
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
      <!-- Pill container -->
      <div
        class="flex items-center justify-between rounded-2xl px-4 sm:px-6 h-14 transition-all duration-300"
        :class="scrolled
          ? 'bg-white/90 backdrop-blur-md shadow-lg shadow-slate-200/60 border border-slate-200/80'
          : 'bg-white/70 backdrop-blur-sm border border-white/60'"
      >
        <!-- Brand -->
        <router-link to="/" class="flex items-center gap-2.5 no-underline">
          <span class="flex items-center justify-center w-8 h-8 rounded-xl bg-primary-600 text-white">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-4 h-4">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
            </svg>
          </span>
          <span class="text-base font-bold text-slate-900 tracking-tight">AthleteIQ</span>
        </router-link>

        <!-- Desktop nav -->
        <nav class="hidden md:flex items-center gap-1">
          <a
            v-for="link in navLinks"
            :key="link.href"
            :href="link.href"
            class="px-3.5 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-all duration-150 no-underline"
            @click.prevent="scrollTo(link.href)"
          >
            {{ link.label }}
          </a>
        </nav>

        <!-- Desktop CTAs -->
        <div class="hidden md:flex items-center gap-2">
          <router-link
            to="/auth/login"
            class="px-4 py-2 text-sm font-semibold text-slate-700 hover:text-slate-900 hover:bg-slate-100 rounded-xl transition-all duration-150 no-underline"
          >
            Log in
          </router-link>
          <router-link
            to="/auth/register"
            class="px-4 py-2 text-sm font-semibold text-white bg-primary-600 hover:bg-primary-700 rounded-xl transition-all duration-150 no-underline shadow-sm"
          >
            Get started
          </router-link>
        </div>

        <!-- Mobile menu button -->
        <button
          class="md:hidden flex items-center justify-center w-11 h-11 rounded-xl text-slate-600 hover:bg-slate-100 transition-colors"
          :aria-label="mobileOpen ? 'Close menu' : 'Open menu'"
          @click="mobileOpen = !mobileOpen"
        >
          <svg v-if="!mobileOpen" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-5 h-5">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-5 h-5">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <!-- Mobile dropdown -->
      <Transition name="dropdown">
        <div
          v-if="mobileOpen"
          class="md:hidden mt-2 rounded-2xl bg-white/95 backdrop-blur-md shadow-xl shadow-slate-200/60 border border-slate-200/80 overflow-hidden"
        >
          <nav class="flex flex-col p-2 gap-0.5">
            <a
              v-for="link in navLinks"
              :key="link.href"
              :href="link.href"
              class="px-4 py-3 text-sm font-medium text-slate-700 hover:text-slate-900 hover:bg-slate-50 rounded-xl transition-all no-underline"
              @click.prevent="mobileLinkClick(link.href)"
            >
              {{ link.label }}
            </a>
          </nav>
          <div class="flex flex-col gap-2 p-3 pt-1 border-t border-slate-100">
            <router-link
              to="/auth/login"
              class="w-full py-2.5 text-center text-sm font-semibold text-slate-700 border border-slate-200 hover:bg-slate-50 rounded-xl transition-all no-underline"
              @click="mobileOpen = false"
            >
              Log in
            </router-link>
            <router-link
              to="/auth/register"
              class="w-full py-2.5 text-center text-sm font-semibold text-white bg-primary-600 hover:bg-primary-700 rounded-xl transition-all no-underline"
              @click="mobileOpen = false"
            >
              Get started
            </router-link>
          </div>
        </div>
      </Transition>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { gsap } from 'gsap'
import { ScrollToPlugin } from 'gsap/ScrollToPlugin'

gsap.registerPlugin(ScrollToPlugin)

const scrolled = ref(false)
const mobileOpen = ref(false)

const navLinks = [
  { label: 'Features', href: '#features' },
  { label: 'How it works', href: '#how-it-works' },
  { label: 'Pathways', href: '#pathways' },
  { label: 'About', href: '#about' }
]

function scrollTo(href: string) {
  const el = document.querySelector(href)
  if (el) {
    gsap.to(window, { scrollTo: { y: el, offsetY: 80 }, duration: 0.9, ease: 'power2.inOut' })
  }
  mobileOpen.value = false
}

function mobileLinkClick(href: string) {
  mobileOpen.value = false
  setTimeout(() => scrollTo(href), 150)
}

function handleScroll() {
  scrolled.value = window.scrollY > 20
}

onMounted(() => window.addEventListener('scroll', handleScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>

<style scoped>
.dropdown-enter-active {
  transition: all 200ms cubic-bezier(0.16, 1, 0.3, 1);
}
.dropdown-leave-active {
  transition: all 150ms ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.98);
}
</style>
