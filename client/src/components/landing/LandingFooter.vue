<template>
  <footer class="border-t border-slate-200 py-8 sm:py-12 px-4 sm:px-6">
    <div class="max-w-6xl mx-auto">
      <!-- Top row -->
      <div class="flex flex-col sm:flex-row items-center justify-between gap-6 sm:gap-8">
        <!-- Brand -->
        <router-link to="/" class="flex items-center no-underline">
          <img src="/athleteiqLogo.svg" alt="AthleteIQ" class="h-6 w-auto" />
        </router-link>

        <!-- Section links -->
        <nav class="flex items-center gap-5">
          <a
            v-for="link in sectionLinks"
            :key="link.href"
            :href="link.href"
            class="text-sm text-slate-500 hover:text-slate-800 no-underline py-1 transition-colors"
            @click.prevent="scrollTo(link.href)"
          >{{ link.label }}</a>
        </nav>

        <!-- Auth links -->
        <div class="flex items-center gap-4">
          <router-link to="/auth/login" class="text-sm text-slate-500 hover:text-slate-800 no-underline py-1 transition-colors">Login</router-link>
          <router-link to="/auth/register" class="text-sm font-semibold text-primary-600 hover:text-primary-700 no-underline py-1 transition-colors">Get started</router-link>
        </div>
      </div>

      <!-- Bottom row -->
      <div class="mt-6 pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400">
        <p>&copy; {{ currentYear }} AthleteIQ. Empowering athlete career transitions.</p>
        <div class="flex items-center gap-4">
          <a href="#" class="hover:text-slate-600 no-underline transition-colors" @click.prevent>Privacy Policy</a>
          <a href="#" class="hover:text-slate-600 no-underline transition-colors" @click.prevent>Terms of Service</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { gsap } from 'gsap'
import { ScrollToPlugin } from 'gsap/ScrollToPlugin'

gsap.registerPlugin(ScrollToPlugin)

const currentYear = new Date().getFullYear()

const sectionLinks = [
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
}
</script>
