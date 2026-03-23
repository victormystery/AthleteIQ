<template>
  <div>
    <!-- Welcome Banner -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary-600 via-primary-700 to-orange-900 p-6 mb-8 text-white shadow-lg shadow-primary-900/20">
      <!-- Decorative circles -->
      <div class="absolute -right-10 -top-10 w-48 h-48 rounded-full bg-white/5 pointer-events-none" />
      <div class="absolute -right-4 top-10 w-28 h-28 rounded-full bg-white/5 pointer-events-none" />

      <div class="relative">
        <div class="flex items-center gap-2 mb-3">
          <span class="text-xs font-semibold uppercase tracking-widest text-primary-200 bg-white/10 px-2.5 py-1 rounded-full">
            {{ roleLabel }}
          </span>
        </div>
        <h1 class="text-2xl font-bold text-white leading-tight">
          {{ greeting }}, {{ user?.name?.split(' ')[0] ?? 'Athlete' }} 👋
        </h1>
        <p class="text-sm text-primary-100 mt-1.5 max-w-lg">
          <template v-if="isAdvisor">
            Review platform insights and help athletes find their ideal career path.
          </template>
          <template v-else>
            Discover career paths perfectly matched to your athletic background and goals.
          </template>
        </p>
        <div v-if="!isAdvisor" class="flex items-center gap-3 mt-4">
          <BaseButton
            variant="secondary"
            size="sm"
            class="!bg-white !text-primary-700 hover:!bg-primary-50 !border-0 !shadow-sm"
            @click="toast.info('Career assessment coming soon!')"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
              <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
              <rect x="9" y="3" width="6" height="4" rx="1"/>
              <path d="M9 12h6M9 16h4"/>
            </svg>
            Take Assessment
          </BaseButton>
          <BaseButton
            variant="ghost"
            size="sm"
            class="!text-white hover:!bg-white/10"
            @click="toast.info('Career pathways coming soon!')"
          >
            Explore Pathways →
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- ── ADVISOR VIEW ──────────────────────────────────────────────────── -->
    <template v-if="isAdvisor">
      <!-- Loading -->
      <div v-if="loadingInsights" class="flex items-center justify-center py-16">
        <AppSpinner size="lg" />
      </div>

      <template v-else-if="insights">
        <!-- Advisor stat cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard label="Total Submissions" :value="insights.totalSubmissions" icon-bg="#ffedd5">
            <template #icon>
              <svg viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2" width="22" height="22">
                <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
                <rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12h6M9 16h4"/>
              </svg>
            </template>
          </StatCard>

          <StatCard label="Feedback Collected" :value="insights.totalFeedback" icon-bg="#dcfce7">
            <template #icon>
              <svg viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" width="22" height="22">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
            </template>
          </StatCard>

          <StatCard label="Avg. Rating" :value="insights.averageRatingOverall ? insights.averageRatingOverall.toFixed(1) + ' / 5' : '—'" icon-bg="#fef3c7">
            <template #icon>
              <svg viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2" width="22" height="22">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
            </template>
          </StatCard>

          <StatCard label="Pathways Analysed" :value="insights.pathwaySummaries?.length ?? 0" icon-bg="#dbeafe">
            <template #icon>
              <svg viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" width="22" height="22">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 8v4l3 3"/>
              </svg>
            </template>
          </StatCard>
        </div>

        <!-- Pathway performance table -->
        <BaseCard title="Pathway Performance" subtitle="Aggregated feedback across all user assessments" class="mb-6">
          <div v-if="insights.pathwaySummaries.length === 0" class="text-center py-10">
            <div class="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-3">
              <svg viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" class="w-6 h-6">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
            </div>
            <p class="text-sm font-medium text-slate-600">No feedback yet</p>
            <p class="text-xs text-slate-400 mt-1">Insights will appear once students submit feedback.</p>
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="p in insights.pathwaySummaries.slice(0, 8)"
              :key="p.pathwaySlug"
              class="flex items-center gap-4 py-2.5 border-b border-slate-100 last:border-0"
            >
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1.5">
                  <p class="text-sm font-semibold text-slate-800 capitalize">
                    {{ formatSlug(p.pathwaySlug) }}
                  </p>
                  <div class="flex items-center gap-3 shrink-0 ml-3">
                    <span class="text-xs font-semibold text-amber-600 flex items-center gap-1">
                      ★ {{ p.averageRating.toFixed(1) }}
                    </span>
                    <span class="text-xs text-slate-400">{{ p.totalFeedback }} reviews</span>
                    <span :class="[
                      'text-xs font-semibold px-2 py-0.5 rounded-full',
                      p.interestedRate >= 70 ? 'bg-green-50 text-green-700' :
                      p.interestedRate >= 40 ? 'bg-amber-50 text-amber-700' : 'bg-red-50 text-red-700'
                    ]">
                      {{ p.interestedRate }}% interested
                    </span>
                  </div>
                </div>
                <div class="w-full bg-slate-100 rounded-full h-1.5">
                  <div
                    class="h-1.5 rounded-full bg-gradient-to-r from-primary-500 to-primary-400 transition-all duration-500"
                    :style="{ width: `${p.interestedRate}%` }"
                  />
                </div>
              </div>
            </div>
          </div>
        </BaseCard>

        <!-- Highlights row -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <BaseCard flat class="!border-primary-100 bg-primary-50/40">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-primary-100 flex items-center justify-center shrink-0">
                <svg viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2" class="w-5 h-5">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-500 font-medium">Top Rated Pathway</p>
                <p class="text-sm font-bold text-slate-800 mt-0.5 capitalize">{{ formatSlug(insights.topRatedPathway) }}</p>
              </div>
            </div>
          </BaseCard>

          <BaseCard flat class="!border-green-100 bg-green-50/40">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-green-100 flex items-center justify-center shrink-0">
                <svg viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" class="w-5 h-5">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-500 font-medium">Most Interesting Pathway</p>
                <p class="text-sm font-bold text-slate-800 mt-0.5 capitalize">{{ formatSlug(insights.mostInterestingPathway) }}</p>
              </div>
            </div>
          </BaseCard>
        </div>
      </template>

      <!-- Error state for advisor -->
      <BaseAlert v-if="insightsError" type="error" :show="!!insightsError">
        {{ insightsError }}
      </BaseAlert>
    </template>

    <!-- ── STUDENT VIEW ──────────────────────────────────────────────────── -->
    <template v-else>
      <!-- Stat cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <StatCard
          label="Assessments Taken"
          :value="assessmentCount"
          icon-bg="#ffedd5"
        >
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2" width="22" height="22">
              <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
              <rect x="9" y="3" width="6" height="4" rx="1"/>
              <path d="M9 14l2 2 4-4"/>
            </svg>
          </template>
        </StatCard>

        <StatCard
          label="Top Match Score"
          :value="topMatchScore ? topMatchScore + '%' : '—'"
          icon-bg="#dcfce7"
        >
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" width="22" height="22">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12 6 12 12 16 14"/>
            </svg>
          </template>
        </StatCard>

        <StatCard
          label="Active Pathways"
          :value="roadmapCount"
          icon-bg="#dbeafe"
        >
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" width="22" height="22">
              <path d="M3 17l4-8 4 4 4-8 4 8"/>
            </svg>
          </template>
        </StatCard>
      </div>

      <!-- Loading state -->
      <div v-if="loadingData" class="flex items-center justify-center py-20">
        <AppSpinner size="lg" />
      </div>

      <template v-else>
        <!-- No assessments: CTA state -->
        <div
          v-if="recommendations.length === 0"
          class="bg-white border-2 border-dashed border-slate-200 rounded-2xl p-10 text-center mb-6"
        >
          <div class="w-16 h-16 rounded-2xl bg-primary-50 flex items-center justify-center mx-auto mb-4">
            <svg viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="1.5" class="w-8 h-8">
              <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
              <rect x="9" y="3" width="6" height="4" rx="1"/>
              <path d="M9 12h6M9 16h4"/>
            </svg>
          </div>
          <h3 class="text-lg font-bold text-slate-800 mb-2">No assessments yet</h3>
          <p class="text-sm text-slate-500 max-w-sm mx-auto mb-6">
            Take your first career assessment to discover pathways that align with your athletic background and skills.
          </p>
          <BaseButton @click="toast.info('Career assessment coming soon!')">
            Take Your First Assessment →
          </BaseButton>
        </div>

        <!-- Content grid with data -->
        <div v-else class="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-6">
          <!-- Left column -->
          <div class="flex flex-col gap-6">
            <!-- Career Recommendations -->
            <BaseCard title="Career Recommendations" subtitle="Based on your most recent assessment">
              <ul class="space-y-3">
                <li
                  v-for="rec in topRecommendations"
                  :key="rec.pathwaySlug"
                  class="group p-3.5 rounded-xl border border-slate-100 hover:border-primary-100 hover:bg-primary-50/30 transition-all duration-150 cursor-pointer"
                  @click="toast.info(`${rec.pathwayName} pathway details coming soon!`)"
                >
                  <div class="flex items-start gap-3">
                    <!-- Rank badge -->
                    <div :class="[
                      'w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold shrink-0 mt-0.5',
                      rec.rank === 1 ? 'bg-amber-100 text-amber-700' :
                      rec.rank === 2 ? 'bg-slate-100 text-slate-600' :
                      'bg-slate-50 text-slate-500'
                    ]">
                      #{{ rec.rank }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center justify-between gap-2 flex-wrap">
                        <p class="text-sm font-semibold text-slate-800">{{ rec.pathwayName }}</p>
                        <span :class="[
                          'text-xs font-bold px-2.5 py-0.5 rounded-full shrink-0',
                          rec.matchPercentage >= 80 ? 'bg-green-50 text-green-700' :
                          rec.matchPercentage >= 60 ? 'bg-primary-50 text-primary-700' :
                          'bg-slate-100 text-slate-600'
                        ]">
                          {{ rec.matchPercentage }}% match
                        </span>
                      </div>
                      <!-- Match bar -->
                      <div class="mt-2 w-full bg-slate-100 rounded-full h-1.5">
                        <div
                          :class="[
                            'h-1.5 rounded-full transition-all duration-700',
                            rec.matchPercentage >= 80 ? 'bg-green-500' :
                            rec.matchPercentage >= 60 ? 'bg-primary-500' : 'bg-slate-400'
                          ]"
                          :style="{ width: `${rec.matchPercentage}%` }"
                        />
                      </div>
                      <!-- Skills -->
                      <div v-if="rec.keySkillsMatch?.length" class="flex flex-wrap gap-1.5 mt-2.5">
                        <span
                          v-for="skill in rec.keySkillsMatch.slice(0, 3)"
                          :key="skill"
                          class="text-[11px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full font-medium"
                        >
                          {{ skill }}
                        </span>
                      </div>
                      <!-- Salary / outlook -->
                      <div v-if="rec.salaryRange || rec.jobGrowthOutlook" class="flex items-center gap-3 mt-2">
                        <span v-if="rec.salaryRange" class="text-xs text-slate-400 flex items-center gap-1">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3 h-3">
                            <line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                          </svg>
                          {{ rec.salaryRange }}
                        </span>
                        <span v-if="rec.jobGrowthOutlook" class="text-xs text-slate-400 flex items-center gap-1">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3 h-3">
                            <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>
                          </svg>
                          {{ rec.jobGrowthOutlook }}
                        </span>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </BaseCard>

            <!-- Roadmap Progress -->
            <BaseCard title="My Active Pathways" subtitle="Career roadmap progress">
              <div v-if="roadmapSummary.length === 0" class="text-center py-8">
                <p class="text-sm text-slate-400">No active pathways yet. Start a roadmap from your recommendations.</p>
              </div>
              <ul v-else class="space-y-4">
                <li
                  v-for="rm in roadmapSummary"
                  :key="rm.pathwaySlug"
                  class="group cursor-pointer"
                  @click="toast.info(`${rm.pathwayTitle} roadmap coming soon!`)"
                >
                  <div class="flex items-center justify-between mb-1.5">
                    <p class="text-sm font-semibold text-slate-800 group-hover:text-primary-700 transition-colors">
                      {{ rm.pathwayTitle }}
                    </p>
                    <span class="text-sm font-bold text-primary-600">{{ rm.overallProgress }}%</span>
                  </div>
                  <div class="w-full bg-slate-100 rounded-full h-2">
                    <div
                      class="h-2 rounded-full bg-gradient-to-r from-primary-500 to-primary-400 transition-all duration-700"
                      :style="{ width: `${rm.overallProgress}%` }"
                    />
                  </div>
                  <p class="text-xs text-slate-400 mt-1.5">
                    Last activity: {{ formatRelativeDate(rm.lastActivityAt) }}
                  </p>
                </li>
              </ul>
            </BaseCard>
          </div>

          <!-- Right column: Quick Actions -->
          <div class="flex flex-col gap-4">
            <BaseCard title="Quick Actions">
              <div class="flex flex-col gap-2.5">
                <BaseButton
                  variant="outline"
                  :block="true"
                  @click="toast.info('Career assessment coming soon!')"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
                    <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                  </svg>
                  New Assessment
                </BaseButton>
                <BaseButton
                  variant="secondary"
                  :block="true"
                  @click="toast.info('Pathways browser coming soon!')"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
                    <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                  </svg>
                  Browse Pathways
                </BaseButton>
                <BaseButton
                  variant="secondary"
                  :block="true"
                  @click="toast.info('Assessment history coming soon!')"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                  </svg>
                  My History
                </BaseButton>
              </div>
            </BaseCard>

            <!-- Top pathway highlight -->
            <div
              v-if="topRecommendations.length > 0"
              class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-4 text-white"
            >
              <p class="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">Best Match</p>
              <p class="text-base font-bold leading-snug">{{ topRecommendations[0].pathwayName }}</p>
              <div class="flex items-center justify-between mt-3">
                <span class="text-2xl font-black text-primary-400">{{ topRecommendations[0].matchPercentage }}%</span>
                <span class="text-xs text-slate-400 text-right leading-tight">match<br>score</span>
              </div>
              <div class="mt-3 w-full bg-white/10 rounded-full h-1.5">
                <div
                  class="h-1.5 rounded-full bg-primary-400"
                  :style="{ width: `${topRecommendations[0].matchPercentage}%` }"
                />
              </div>
            </div>
          </div>
        </div>
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStore'
import { useToast } from '@/composables/useToast'
import careerService, { type CareerRecommendation, type RecommendationItem } from '@/services/career.service'
import roadmapService, { type RoadmapSummaryItem } from '@/services/roadmap.service'
import feedbackLoopService, { type FeedbackInsights } from '@/services/feedbackLoop.service'
import StatCard from '@/components/StatCard.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import AppSpinner from '@/components/AppSpinner.vue'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)
const toast = useToast()

const isAdvisor = computed(() =>
  user.value?.role === 'career_advisor' || user.value?.role === 'admin'
)

const roleLabel = computed(() => {
  const map: Record<string, string> = {
    student: 'Student',
    career_advisor: 'Career Advisor',
    admin: 'Administrator'
  }
  return map[user.value?.role ?? ''] ?? 'Member'
})

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Good morning'
  if (h < 17) return 'Good afternoon'
  return 'Good evening'
})

// ── Student data ─────────────────────────────────────────────────────────────
const loadingData = ref(false)
const recommendations = ref<CareerRecommendation[]>([])
const roadmapSummary = ref<RoadmapSummaryItem[]>([])

const topRecommendations = computed((): RecommendationItem[] => {
  if (!recommendations.value.length) return []
  return recommendations.value[0]?.recommendations?.slice(0, 5) ?? []
})

const assessmentCount = computed(() => recommendations.value.length)
const roadmapCount = computed(() => roadmapSummary.value.length)
const topMatchScore = computed(() => topRecommendations.value[0]?.matchPercentage ?? 0)

// ── Advisor data ──────────────────────────────────────────────────────────────
const loadingInsights = ref(false)
const insights = ref<FeedbackInsights | null>(null)
const insightsError = ref('')

// ── Helpers ───────────────────────────────────────────────────────────────────
function formatSlug(slug: string): string {
  return slug
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ')
}

function formatRelativeDate(iso: string): string {
  if (!iso) return 'N/A'
  const d = new Date(iso)
  const now = new Date()
  const diff = Math.floor((now.getTime() - d.getTime()) / (1000 * 60 * 60 * 24))
  if (diff === 0) return 'Today'
  if (diff === 1) return 'Yesterday'
  if (diff < 7) return `${diff} days ago`
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  if (isAdvisor.value) {
    loadingInsights.value = true
    insightsError.value = ''
    try {
      const { data } = await feedbackLoopService.getInsights()
      insights.value = data.data.insights
    } catch {
      insightsError.value = 'Unable to load platform insights. Please try again.'
    } finally {
      loadingInsights.value = false
    }
  } else {
    loadingData.value = true
    try {
      const [recRes, roadRes] = await Promise.allSettled([
        careerService.getRecommendations(),
        roadmapService.getSummary()
      ])
      if (recRes.status === 'fulfilled') {
        recommendations.value = recRes.value.data.data.recommendations ?? []
      }
      if (roadRes.status === 'fulfilled') {
        roadmapSummary.value = roadRes.value.data.data.summary ?? []
      }
    } finally {
      loadingData.value = false
    }
  }
})
</script>
