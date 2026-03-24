<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Career Pathways</h1>
        <p class="text-sm text-slate-500 mt-0.5">
          <span v-if="pathways.length">{{ pathways.length }} pathways in the catalogue</span>
          <span v-else>Loading…</span>
        </p>
      </div>
      <router-link
        to="/admin"
        class="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 font-medium transition-colors"
      >
        <svg viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4">
          <path fill-rule="evenodd" d="M17 10a.75.75 0 0 1-.75.75H5.612l4.158 3.96a.75.75 0 1 1-1.04 1.08l-5.5-5.25a.75.75 0 0 1 0-1.08l5.5-5.25a.75.75 0 1 1 1.04 1.08L5.612 9.25H16.25A.75.75 0 0 1 17 10z" clip-rule="evenodd"/>
        </svg>
        Back to Overview
      </router-link>
    </div>

    <!-- Error -->
    <BaseAlert v-if="error" type="error" :show="!!error" class="mb-6">{{ error }}</BaseAlert>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-24">
      <AppSpinner size="lg" />
    </div>

    <!-- Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <div
        v-for="p in pathways"
        :key="p._id"
        class="bg-white border border-slate-200 rounded-xl overflow-hidden hover:shadow-md hover:-translate-y-0.5 transition-all duration-200"
      >
        <!-- Colour bar -->
        <div class="h-1.5" :style="{ backgroundColor: p.colour || '#f97316' }" />
        <div class="p-5">
          <!-- Title row -->
          <div class="flex items-start gap-3 mb-3">
            <span class="text-2xl leading-none shrink-0">{{ p.icon }}</span>
            <div class="min-w-0">
              <h3 class="text-sm font-bold text-slate-800 leading-snug">{{ p.title }}</h3>
              <p class="text-xs text-slate-400 mt-0.5 font-mono">{{ p.slug }}</p>
            </div>
            <span :class="[
              'ml-auto shrink-0 text-[10px] font-bold px-2 py-0.5 rounded-full',
              p.isActive ? 'bg-green-50 text-green-700' : 'bg-slate-100 text-slate-500'
            ]">
              {{ p.isActive ? 'Active' : 'Inactive' }}
            </span>
          </div>

          <!-- Description -->
          <p class="text-xs text-slate-500 leading-relaxed line-clamp-2 mb-4">{{ p.description }}</p>

          <!-- Meta pills -->
          <div class="flex flex-wrap gap-1.5 mb-4">
            <span class="text-[10px] font-semibold bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">
              {{ p.category }}
            </span>
            <span class="text-[10px] font-semibold bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">
              {{ p.jobOutlook }}
            </span>
            <span class="text-[10px] font-semibold bg-primary-50 text-primary-600 px-2 py-0.5 rounded-full">
              {{ formatSalary(p.salaryRange) }}
            </span>
          </div>

          <!-- Divider -->
          <div class="border-t border-slate-100 pt-3">
            <!-- Key skills (max 3) -->
            <p class="text-[10px] font-bold uppercase tracking-wide text-slate-400 mb-1.5">Key Skills</p>
            <div class="flex flex-wrap gap-1">
              <span
                v-for="skill in p.keySkills.slice(0, 4)"
                :key="skill"
                class="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded font-medium"
              >{{ skill }}</span>
              <span v-if="p.keySkills.length > 4" class="text-[10px] text-slate-400 font-medium px-1">
                +{{ p.keySkills.length - 4 }} more
              </span>
            </div>
          </div>

          <!-- Stats row -->
          <div class="flex items-center justify-between mt-3 pt-3 border-t border-slate-100 text-xs text-slate-400">
            <span>{{ p.careerProgressionSteps?.length ?? 0 }} progression steps</span>
            <span>{{ p.successStories?.length ?? 0 }} success stories</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import careerService, { type CareerPathway } from '@/services/career.service'
import BaseAlert from '@/components/BaseAlert.vue'
import AppSpinner from '@/components/AppSpinner.vue'

const pathways = ref<CareerPathway[]>([])
const loading = ref(false)
const error = ref('')

function formatSalary(range: { min: number; max: number; currency: string } | undefined): string {
  if (!range) return '—'
  const fmt = (n: number) => n >= 1000 ? `$${Math.round(n / 1000)}k` : `$${n}`
  return `${fmt(range.min)}–${fmt(range.max)} ${range.currency}`
}

onMounted(async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await careerService.getPathways()
    pathways.value = data.data.pathways ?? []
  } catch (e: unknown) {
    const err = e as { response?: { data?: { message?: string } } }
    error.value = err.response?.data?.message ?? 'Failed to load pathways.'
  } finally {
    loading.value = false
  }
})
</script>
