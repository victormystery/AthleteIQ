<template>
  <section ref="sectionRef" id="features" class="py-16 md:py-24 px-4 sm:px-6 bg-slate-50">
    <div class="max-w-6xl mx-auto">
      <div ref="headerRef" class="text-center mb-10 md:mb-16">
        <p class="text-sm font-bold uppercase tracking-widest text-primary-600 mb-3">Features</p>
        <h2 class="text-3xl xs:text-4xl sm:text-5xl font-black text-slate-900 tracking-tight">
          Built for athletes, by design
        </h2>
        <p class="mt-4 text-base sm:text-lg text-slate-500 max-w-xl mx-auto">
          Every feature is crafted around the unique transition athletes face when moving beyond competition.
        </p>
      </div>

      <div ref="gridRef" class="grid md:grid-cols-3 gap-5 md:gap-6">
        <div
          v-for="feature in features"
          :key="feature.title"
          class="feature-card group bg-white rounded-3xl p-6 md:p-8 border border-slate-200 hover:border-primary-200 hover:shadow-xl hover:shadow-primary-50 transition-all duration-300 hover:-translate-y-1"
        >
          <div class="w-16 h-16 rounded-2xl flex items-center justify-center mb-5 md:mb-6" :class="feature.iconBg">
            <span class="text-3xl leading-none select-none">{{ feature.icon }}</span>
          </div>
          <h3 class="text-lg sm:text-xl font-bold text-slate-900 mb-2 sm:mb-3">{{ feature.title }}</h3>
          <p class="text-sm sm:text-base text-slate-500 leading-relaxed">{{ feature.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, ref } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { features } from '@/data/landingData'

gsap.registerPlugin(ScrollTrigger)

const sectionRef = ref<HTMLElement | null>(null)
const headerRef  = ref<HTMLElement | null>(null)
const gridRef    = ref<HTMLElement | null>(null)

let ctx: gsap.Context

onMounted(async () => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  await nextTick()
  if (!sectionRef.value) return

  ctx = gsap.context(() => {
    if (headerRef.value) {
      gsap.fromTo(headerRef.value as Element, {
        autoAlpha: 0,
        y: 32
      }, {
        autoAlpha: 1,
        y: 0,
        duration: 0.7,
        ease: 'power3.out',
        scrollTrigger: { trigger: sectionRef.value as Element, start: 'top 82%', once: true }
      })
    }
    if (gridRef.value) {
      gsap.fromTo(gridRef.value.querySelectorAll('.feature-card'), {
        autoAlpha: 0,
        y: 44
      }, {
        autoAlpha: 1,
        y: 0,
        duration: 0.65,
        ease: 'power3.out',
        stagger: 0.15,
        scrollTrigger: { trigger: sectionRef.value as Element, start: 'top 72%', once: true }
      })
    }
  }, sectionRef.value as Element)

  ScrollTrigger.refresh()
})

onUnmounted(() => ctx?.revert())
</script>
