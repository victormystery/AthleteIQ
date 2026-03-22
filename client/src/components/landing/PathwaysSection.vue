<template>
  <section ref="sectionRef" id="pathways" class="py-16 md:py-24 px-4 sm:px-6 bg-slate-50">
    <div class="max-w-6xl mx-auto">
      <div ref="headerRef" class="text-center mb-10 md:mb-16">
        <p class="text-sm font-bold uppercase tracking-widest text-primary-600 mb-3">Pathways</p>
        <h2 class="text-3xl xs:text-4xl sm:text-5xl font-black text-slate-900 tracking-tight">
          11 career pathways explored
        </h2>
        <p class="mt-4 text-base sm:text-lg text-slate-500 max-w-xl mx-auto">
          From coaching to sports law, we map every route from the field to a fulfilling career.
        </p>
      </div>

      <div ref="gridRef" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div
          v-for="pathway in pathways"
          :key="pathway.title"
          class="pathway-card group bg-white rounded-3xl p-5 sm:p-6 border border-slate-200 hover:border-primary-300 hover:shadow-lg hover:shadow-slate-100 transition-all duration-300 cursor-pointer"
          @click="router.push('/auth/register')"
        >
          <div class="flex items-center gap-3 sm:gap-4 mb-4">
            <div class="w-11 h-11 rounded-2xl flex items-center justify-center text-xl shrink-0" :class="pathway.bg">
              {{ pathway.emoji }}
            </div>
            <div class="min-w-0">
              <h3 class="text-sm font-bold text-slate-900 truncate">{{ pathway.title }}</h3>
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

      <div ref="ctaRef" class="text-center mt-8 sm:mt-10">
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
</template>

<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { pathways } from '@/data/landingData'

gsap.registerPlugin(ScrollTrigger)

const router = useRouter()

const sectionRef = ref<HTMLElement | null>(null)
const headerRef  = ref<HTMLElement | null>(null)
const gridRef    = ref<HTMLElement | null>(null)
const ctaRef     = ref<HTMLElement | null>(null)

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
      gsap.fromTo(gridRef.value.querySelectorAll('.pathway-card'), {
        autoAlpha: 0,
        y: 40
      }, {
        autoAlpha: 1,
        y: 0,
        duration: 0.6,
        ease: 'power3.out',
        stagger: 0.08,
        scrollTrigger: { trigger: sectionRef.value as Element, start: 'top 72%', once: true }
      })
    }
    if (ctaRef.value) {
      gsap.fromTo(ctaRef.value as Element, {
        autoAlpha: 0,
        y: 20
      }, {
        autoAlpha: 1,
        y: 0,
        duration: 0.5,
        ease: 'power3.out',
        scrollTrigger: { trigger: sectionRef.value as Element, start: 'top 68%', once: true }
      })
    }
  }, sectionRef.value as Element)

  ScrollTrigger.refresh()
})

onUnmounted(() => ctx?.revert())
</script>
