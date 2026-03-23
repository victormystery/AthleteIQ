<template>
  <div class="space-y-6">
    <!-- Back -->
    <router-link
      to="/app/pathways"
      class="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-700 transition-colors"
    >
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
        <polyline points="15 18 9 12 15 6"/>
      </svg>
      Back to Pathways
    </router-link>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
      <p class="text-red-700">{{ error }}</p>
    </div>

    <template v-else-if="roadmap">
      <!-- Header -->
      <div class="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h2 class="text-2xl font-bold text-slate-800">{{ roadmap.pathwayTitle }}</h2>
          <p class="text-slate-500 mt-1">Your personalised roadmap · {{ completedCount }}/{{ roadmap.milestones.length }} milestones completed</p>
        </div>
        <router-link
          :to="`/app/pathways/${roadmap.pathwaySlug}`"
          class="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1"
        >
          View pathway details
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </router-link>
      </div>

      <!-- Progress bar -->
      <div class="bg-white border border-slate-200 rounded-xl p-4">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-slate-700">Overall Progress</span>
          <span class="text-sm font-bold text-primary-600">{{ overallProgress }}%</span>
        </div>
        <div class="h-2.5 bg-slate-100 rounded-full overflow-hidden">
          <div
            class="h-full bg-primary-500 rounded-full transition-all duration-500"
            :style="{ width: overallProgress + '%' }"
          />
        </div>
      </div>

      <!-- Milestones -->
      <div class="relative">
        <div class="absolute left-6 top-8 bottom-8 w-0.5 bg-slate-100" />
        <div class="space-y-4">
          <div
            v-for="milestone in roadmap.milestones"
            :key="milestone.id"
            :class="[
              'relative bg-white border rounded-xl p-5 pl-16 transition-all',
              milestone.status === 'completed' ? 'border-green-200' :
              milestone.status === 'in_progress' ? 'border-primary-200' :
              'border-slate-200'
            ]"
          >
            <!-- Status dot -->
            <div
              :class="[
                'absolute left-2.5 top-5 w-7 h-7 rounded-full flex items-center justify-center border-2 bg-white z-10',
                milestone.status === 'completed' ? 'border-green-500 text-green-500' :
                milestone.status === 'in_progress' ? 'border-primary-500 text-primary-500' :
                'border-slate-300 text-slate-300'
              ]"
            >
              <svg v-if="milestone.status === 'completed'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-3.5 h-3.5">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <svg v-else-if="milestone.status === 'in_progress'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="w-3.5 h-3.5">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
              <div v-else class="w-2.5 h-2.5 rounded-full bg-slate-300" />
            </div>

            <div class="flex items-start justify-between gap-4 flex-wrap">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 flex-wrap">
                  <h3 class="text-sm font-semibold text-slate-800">{{ milestone.title }}</h3>
                  <span
                    :class="[
                      'text-xs px-2 py-0.5 rounded-full font-medium',
                      milestone.status === 'completed' ? 'bg-green-100 text-green-700' :
                      milestone.status === 'in_progress' ? 'bg-primary-100 text-primary-700' :
                      'bg-slate-100 text-slate-500'
                    ]"
                  >{{ statusLabel(milestone.status) }}</span>
                  <span class="text-xs bg-slate-100 text-slate-400 px-2 py-0.5 rounded-full">{{ milestone.type }}</span>
                </div>

                <p class="text-sm text-slate-600 mt-1">{{ milestone.description }}</p>

                <div class="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-400">
                  <span class="flex items-center gap-1">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5">
                      <circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/>
                    </svg>
                    {{ milestone.duration }}
                  </span>
                  <span v-if="milestone.estimatedCost" class="flex items-center gap-1">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5">
                      <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                    </svg>
                    {{ milestone.estimatedCost }}
                  </span>
                </div>

                <!-- Resources -->
                <div v-if="milestone.resources?.length" class="mt-3 flex flex-wrap gap-2">
                  <a
                    v-for="res in milestone.resources"
                    :key="res.url"
                    :href="res.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-xs text-primary-600 hover:text-primary-700 flex items-center gap-1 underline"
                  >
                    {{ res.name }}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3 h-3">
                      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                      <polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
                    </svg>
                  </a>
                </div>

                <!-- Notes -->
                <p v-if="milestone.notes" class="mt-2 text-xs text-slate-500 italic">{{ milestone.notes }}</p>
                <p v-if="milestone.completedAt" class="mt-1 text-xs text-green-600">
                  Completed {{ formatDate(milestone.completedAt) }}
                </p>
              </div>

              <!-- Status actions -->
              <div class="shrink-0">
                <div v-if="updatingId === milestone.id" class="w-5 h-5 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
                <div v-else class="flex flex-col gap-1.5">
                  <button
                    v-if="milestone.status !== 'completed'"
                    class="text-xs py-1.5 px-3 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors font-medium"
                    @click="updateStatus(milestone, 'completed')"
                  >Mark done</button>
                  <button
                    v-if="milestone.status === 'not_started'"
                    class="text-xs py-1.5 px-3 border border-primary-300 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors font-medium"
                    @click="updateStatus(milestone, 'in_progress')"
                  >Start</button>
                  <button
                    v-if="milestone.status !== 'not_started'"
                    class="text-xs py-1.5 px-3 border border-slate-200 text-slate-500 hover:bg-slate-50 rounded-lg transition-colors"
                    @click="updateStatus(milestone, 'not_started')"
                  >Reset</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import roadmapService, { type Roadmap, type RoadmapMilestone, type MilestoneStatus } from '@/services/roadmap.service'

const route = useRoute()
const loading = ref(false)
const error = ref('')
const roadmap = ref<Roadmap | null>(null)
const updatingId = ref<string | null>(null)

const completedCount = computed(() =>
  roadmap.value?.milestones.filter(m => m.status === 'completed').length ?? 0
)

const overallProgress = computed(() => {
  if (!roadmap.value?.milestones.length) return 0
  return Math.round((completedCount.value / roadmap.value.milestones.length) * 100)
})

function statusLabel(status: MilestoneStatus): string {
  return { not_started: 'Not started', in_progress: 'In progress', completed: 'Completed' }[status]
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-AU', { day: 'numeric', month: 'short', year: 'numeric' })
}

async function updateStatus(milestone: RoadmapMilestone, status: MilestoneStatus) {
  if (!roadmap.value) return
  updatingId.value = milestone.id
  try {
    await roadmapService.updateProgress(roadmap.value.pathwaySlug, {
      milestoneId: milestone.id,
      milestoneTitle: milestone.title,
      status
    })
    milestone.status = status
    if (status === 'completed') {
      milestone.completedAt = new Date().toISOString()
    } else {
      milestone.completedAt = undefined
    }
  } catch {
    // silently ignore — status already correct in UI if no error boundary
  } finally {
    updatingId.value = null
  }
}

onMounted(async () => {
  loading.value = true
  try {
    const slug = route.params.slug as string
    const res = await roadmapService.getPathwayRoadmap(slug)
    roadmap.value = res.data.data.roadmap
  } catch (e: unknown) {
    const err = e as { response?: { data?: { message?: string } } }
    error.value = err.response?.data?.message ?? 'Failed to load roadmap.'
  } finally {
    loading.value = false
  }
})
</script>
