<template>
  <section ref="sectionRef" class="py-12 md:py-20 px-4 sm:px-6">
    <div class="max-w-5xl mx-auto">
      <div ref="bannerRef" class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary-600 to-primary-800 px-6 py-12 sm:px-8 sm:py-16 text-center shadow-2xl shadow-primary-200">
        <!-- Decorative circles -->
        <div class="absolute -top-16 -right-16 w-64 h-64 bg-white/10 rounded-full" />
        <div class="absolute -bottom-12 -left-12 w-48 h-48 bg-white/10 rounded-full" />

        <div class="relative z-10">
          <h2 class="text-3xl xs:text-4xl sm:text-5xl font-black text-white tracking-tight">
            Ready to find your path?
          </h2>
          <p class="mt-4 text-base sm:text-lg text-primary-200 max-w-xl mx-auto">
            Complete the 5-minute assessment and get personalised career recommendations instantly.
          </p>
          <div class="mt-8 sm:mt-10 flex flex-col sm:flex-row items-stretch sm:items-center justify-center gap-3">
            <router-link
              to="/auth/register"
              class="inline-flex items-center justify-center gap-2 px-7 py-3.5 text-base font-semibold text-primary-700 bg-white hover:bg-primary-50 rounded-2xl transition-all no-underline shadow-lg"
            >
              Create free account
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-4 h-4">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </router-link>
            <router-link
              to="/auth/login"
              class="inline-flex items-center justify-center gap-2 px-7 py-3.5 text-base font-semibold text-white/80 hover:text-white border border-white/30 hover:border-white/60 rounded-2xl transition-all no-underline"
            >
              Already have an account
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, ref } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const sectionRef = ref<HTMLElement | null>(null)
const bannerRef  = ref<HTMLElement | null>(null)

let ctx: gsap.Context

onMounted(async () => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  await nextTick()
  if (!sectionRef.value || !bannerRef.value) return

  ctx = gsap.context(() => {
    gsap.from(bannerRef.value as Element, {
      opacity: 0, y: 50, scale: 0.97, duration: 0.8, ease: 'power3.out',
      scrollTrigger: { trigger: bannerRef.value as Element, start: 'top 90%', once: true }
    })
  }, sectionRef.value as Element)
})

onUnmounted(() => ctx?.revert())
</script>
