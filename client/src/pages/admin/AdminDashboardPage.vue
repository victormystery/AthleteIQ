<template>
  <div>
    <!-- Page header -->
    <div class="flex items-start justify-between mb-8 gap-4 flex-wrap">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">Platform Overview</h1>
        <p class="text-sm text-slate-500 mt-0.5">Monitor usage, growth, and activity across AthleteIQ.</p>
      </div>
      <div class="flex items-center gap-2 text-xs text-slate-400 bg-white border border-slate-200 px-3 py-1.5 rounded-lg shadow-sm">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 6v6l4 2"/>
        </svg>
        Updated just now
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading && !stats" class="flex items-center justify-center py-24">
      <AppSpinner size="lg" />
    </div>

    <!-- Error -->
    <BaseAlert v-if="error" type="error" :show="!!error" dismissible @dismiss="error = null">
      {{ error }}
    </BaseAlert>

    <template v-if="stats">
      <!-- Stat cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <StatCard label="Total Users" :value="stats.totalUsers" icon-bg="#ffedd5">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2" width="22" height="22">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
          </template>
        </StatCard>

        <StatCard label="Students" :value="stats.totalStudents" icon-bg="#dcfce7">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" width="22" height="22">
              <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
              <path d="M6 12v5c0 2 6 3 6 3s6-1 6-3v-5"/>
            </svg>
          </template>
        </StatCard>

        <StatCard label="Advisors" :value="stats.totalAdvisors" icon-bg="#dbeafe">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" width="22" height="22">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </template>
        </StatCard>

        <StatCard label="Assessments" :value="stats.totalAssessments" icon-bg="#fef3c7">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2" width="22" height="22">
              <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
              <rect x="9" y="3" width="6" height="4" rx="1"/>
              <path d="M9 14l2 2 4-4"/>
            </svg>
          </template>
        </StatCard>

        <StatCard label="Feedback" :value="stats.totalFeedback" icon-bg="#fce7f3">
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" stroke="#db2777" stroke-width="2" width="22" height="22">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </template>
        </StatCard>
      </div>

      <!-- System Health -->
      <div class="mb-8">
        <div class="flex items-center justify-between mb-3">
          <p class="text-xs font-bold uppercase tracking-widest text-slate-400">System Health</p>
          <button
            class="text-xs text-primary-500 font-semibold hover:text-primary-700 transition-colors flex items-center gap-1"
            :disabled="healthLoading"
            @click="refreshHealth"
          >
            <svg :class="['w-3.5 h-3.5', healthLoading ? 'animate-spin' : '']" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M23 4v6h-6"/><path d="M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
            </svg>
            Refresh
          </button>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <!-- API Server -->
          <div class="bg-white rounded-xl border border-slate-200 px-4 py-3.5 flex items-center gap-3">
            <div :class="['w-2.5 h-2.5 rounded-full shrink-0', health ? 'bg-green-400' : healthError ? 'bg-red-400' : 'bg-slate-300']" />
            <div class="min-w-0">
              <p class="text-xs font-semibold text-slate-500">API Server</p>
              <p :class="['text-sm font-bold mt-0.5', health ? 'text-green-700' : healthError ? 'text-red-600' : 'text-slate-400']">
                {{ healthLoading ? 'Checking…' : health ? 'Operational' : healthError ? 'Unreachable' : 'Unknown' }}
              </p>
            </div>
            <span v-if="health" class="ml-auto text-xs text-slate-400 shrink-0">{{ health.env }}</span>
          </div>

          <!-- Database -->
          <div class="bg-white rounded-xl border border-slate-200 px-4 py-3.5 flex items-center gap-3">
            <div :class="['w-2.5 h-2.5 rounded-full shrink-0', health ? 'bg-green-400' : healthError ? 'bg-red-400' : 'bg-slate-300']" />
            <div class="min-w-0">
              <p class="text-xs font-semibold text-slate-500">Database</p>
              <p :class="['text-sm font-bold mt-0.5', health ? 'text-green-700' : healthError ? 'text-red-600' : 'text-slate-400']">
                {{ healthLoading ? 'Checking…' : health ? 'Connected' : healthError ? 'Unreachable' : 'Unknown' }}
              </p>
            </div>
          </div>

          <!-- Last checked -->
          <div class="bg-white rounded-xl border border-slate-200 px-4 py-3.5 flex items-center gap-3">
            <div class="w-2.5 h-2.5 rounded-full bg-primary-300 shrink-0" />
            <div class="min-w-0">
              <p class="text-xs font-semibold text-slate-500">Last Checked</p>
              <p class="text-sm font-bold text-slate-700 mt-0.5">
                {{ health ? formatHealthTime(health.timestamp) : healthLoading ? '…' : '—' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Role distribution card -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
        <BaseCard title="User Distribution" subtitle="Breakdown by account type" class="lg:col-span-1">
          <div class="space-y-4">
            <!-- Students -->
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                  <span class="text-sm font-medium text-slate-700">Students</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs text-slate-400">{{ stats.totalStudents }}</span>
                  <span class="text-xs font-semibold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded-full">
                    {{ totalMembersCount ? Math.round((stats.totalStudents / totalMembersCount) * 100) : 0 }}%
                  </span>
                </div>
              </div>
              <div class="w-full bg-slate-100 rounded-full h-2">
                <div
                  class="h-2 rounded-full bg-emerald-500 transition-all duration-700"
                  :style="{ width: totalMembersCount ? `${(stats.totalStudents / totalMembersCount) * 100}%` : '0%' }"
                />
              </div>
            </div>

            <!-- Advisors -->
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-blue-500" />
                  <span class="text-sm font-medium text-slate-700">Advisors</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs text-slate-400">{{ stats.totalAdvisors }}</span>
                  <span class="text-xs font-semibold text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded-full">
                    {{ totalMembersCount ? Math.round((stats.totalAdvisors / totalMembersCount) * 100) : 0 }}%
                  </span>
                </div>
              </div>
              <div class="w-full bg-slate-100 rounded-full h-2">
                <div
                  class="h-2 rounded-full bg-blue-500 transition-all duration-700"
                  :style="{ width: totalMembersCount ? `${(stats.totalAdvisors / totalMembersCount) * 100}%` : '0%' }"
                />
              </div>
            </div>

            <!-- Admins -->
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full bg-amber-500" />
                  <span class="text-sm font-medium text-slate-700">Admins</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs text-slate-400">{{ adminCount }}</span>
                  <span class="text-xs font-semibold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded-full">
                    {{ totalMembersCount ? Math.round((adminCount / totalMembersCount) * 100) : 0 }}%
                  </span>
                </div>
              </div>
              <div class="w-full bg-slate-100 rounded-full h-2">
                <div
                  class="h-2 rounded-full bg-amber-500 transition-all duration-700"
                  :style="{ width: totalMembersCount ? `${(adminCount / totalMembersCount) * 100}%` : '0%' }"
                />
              </div>
            </div>
          </div>

          <!-- Engagement ratio -->
          <div class="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between">
            <span class="text-xs text-slate-500">Assessment engagement</span>
            <span class="text-sm font-bold text-primary-600">
              {{ stats.totalStudents > 0 ? Math.round((stats.totalAssessments / stats.totalStudents) * 100) : 0 }}%
            </span>
          </div>
        </BaseCard>

        <!-- Recent users + assessments grid -->
        <div class="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- Quick metrics -->
          <div class="bg-gradient-to-br from-primary-600 to-primary-800 rounded-xl p-5 text-white">
            <p class="text-xs font-semibold text-primary-200 uppercase tracking-widest mb-3">Assessments per User</p>
            <p class="text-4xl font-black">
              {{ stats.totalStudents > 0 ? (stats.totalAssessments / stats.totalStudents).toFixed(1) : '0' }}
            </p>
            <p class="text-xs text-primary-200 mt-1">avg. assessments / student</p>
          </div>

          <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-5 text-white">
            <p class="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-3">Feedback Rate</p>
            <p class="text-4xl font-black">
              {{ stats.totalAssessments > 0 ? Math.round((stats.totalFeedback / stats.totalAssessments) * 100) : 0 }}%
            </p>
            <p class="text-xs text-slate-400 mt-1">of assessments received feedback</p>
          </div>
        </div>
      </div>

      <!-- Main content grid -->
      <div class="grid grid-cols-1 lg:grid-cols-[1fr_360px] gap-6">
        <!-- Recent Users -->
        <BaseCard title="Recent Registrations" subtitle="Latest users to join the platform">
          <template #actions>
            <router-link
              to="/admin/users"
              class="text-sm text-primary-600 font-semibold hover:text-primary-700 transition-colors flex items-center gap-1"
            >
              View all
              <svg viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5">
                <path fill-rule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10z" clip-rule="evenodd"/>
              </svg>
            </router-link>
          </template>

          <div v-if="recentUsers.length === 0" class="text-center py-10">
            <p class="text-sm text-slate-400">No users found</p>
          </div>

          <ul v-else class="divide-y divide-slate-100 -mx-6 -mb-6">
            <li
              v-for="u in recentUsers"
              :key="u._id"
              class="flex items-center gap-3 px-6 py-3.5 hover:bg-slate-50 transition-colors first:pt-3.5 last:pb-3.5"
            >
              <UserAvatar :name="u.name" size="sm" />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-slate-800 truncate">{{ u.name }}</p>
                <p class="text-xs text-slate-400 mt-0.5 truncate">{{ u.email }}</p>
              </div>
              <div class="flex items-center gap-2 shrink-0">
                <span :class="roleBadgeClass(u.role)" class="text-[11px] px-2.5 py-0.5 rounded-full font-semibold">
                  {{ formatRole(u.role) }}
                </span>
                <span class="text-xs text-slate-400 hidden sm:block">{{ formatDate(u.createdAt) }}</span>
              </div>
            </li>
          </ul>
        </BaseCard>

        <!-- Recent Assessments -->
        <BaseCard title="Recent Assessments" subtitle="Latest career assessments submitted">
          <div v-if="assessments.length === 0" class="text-center py-10">
            <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-3">
              <svg viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" class="w-5 h-5">
                <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
                <rect x="9" y="3" width="6" height="4" rx="1"/>
              </svg>
            </div>
            <p class="text-sm text-slate-400">No assessments yet</p>
          </div>

          <ul v-else class="space-y-3">
            <li
              v-for="a in assessments"
              :key="a._id"
              class="bg-slate-50 rounded-xl border border-slate-100 overflow-hidden"
            >
              <!-- Header row (always visible) -->
              <div
                class="flex items-center gap-2.5 px-3 pt-3 pb-2.5 cursor-pointer hover:bg-slate-100 transition-colors"
                @click="toggleAssessment(a._id)"
              >
                <UserAvatar :name="a.user?.name ?? 'Unknown'" size="sm" />
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-semibold text-slate-800 truncate">{{ a.user?.name ?? 'Unknown User' }}</p>
                  <p class="text-xs text-slate-400 mt-0.5">{{ formatDate(a.createdAt) }}</p>
                </div>
                <svg
                  :class="['w-4 h-4 text-slate-400 transition-transform shrink-0', expandedAssessment === a._id ? 'rotate-180' : '']"
                  viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                >
                  <polyline points="6 9 12 15 18 9"/>
                </svg>
              </div>
              <!-- Tags -->
              <div v-if="a.questionnaireResponse" class="flex flex-wrap gap-1.5 px-3 pb-2.5 ml-[calc(2rem+10px)]">
                <span v-if="a.questionnaireResponse.primary_sport" class="text-[11px] bg-primary-100 text-primary-700 px-2 py-0.5 rounded-full font-semibold">
                  {{ a.questionnaireResponse.primary_sport }}
                </span>
                <span v-if="a.questionnaireResponse.academic_level" class="text-[11px] bg-slate-200 text-slate-600 px-2 py-0.5 rounded-full font-medium">
                  {{ a.questionnaireResponse.academic_level }}
                </span>
              </div>
              <!-- Expanded detail: all 14 fields -->
              <div v-if="expandedAssessment === a._id && a.questionnaireResponse" class="px-3 pb-3 border-t border-slate-200 pt-3 mt-1">
                <div class="grid grid-cols-2 gap-x-4 gap-y-2">
                  <div v-for="field in getAssessmentFields(a.questionnaireResponse)" :key="field.label">
                    <p class="text-[10px] font-bold uppercase tracking-wide text-slate-400">{{ field.label }}</p>
                    <p class="text-xs font-semibold text-slate-700 mt-0.5">{{ field.value }}</p>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </BaseCard>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAdminStore } from '@/stores/adminStore'
import adminService from '@/services/admin.service'
import StatCard from '@/components/StatCard.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import AppSpinner from '@/components/AppSpinner.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import type { QuestionnaireResponseData, SystemHealth } from '@/types'

const adminStore = useAdminStore()
const { stats, recentUsers, assessments, loading, error } = storeToRefs(adminStore)

const totalMembersCount = computed(() => stats.value?.totalUsers ?? 0)
const adminCount = computed(() => {
  if (!stats.value) return 0
  return Math.max(0, stats.value.totalUsers - stats.value.totalStudents - stats.value.totalAdvisors)
})

// ── System Health ─────────────────────────────────────────────────────────────
const health = ref<SystemHealth | null>(null)
const healthError = ref(false)
const healthLoading = ref(false)

async function refreshHealth() {
  healthLoading.value = true
  healthError.value = false
  try {
    const { data } = await adminService.getSystemHealth()
    health.value = data
  } catch {
    healthError.value = true
    health.value = null
  } finally {
    healthLoading.value = false
  }
}

function formatHealthTime(iso: string): string {
  return new Date(iso).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

// ── Expandable Assessments ────────────────────────────────────────────────────
const expandedAssessment = ref<string | null>(null)

function toggleAssessment(id: string) {
  expandedAssessment.value = expandedAssessment.value === id ? null : id
}

function getAssessmentFields(q: QuestionnaireResponseData) {
  return [
    { label: 'What is your primary sport of interest?', value: q.primary_sport ?? '—' },
    { label: 'What is your current academic level?', value: q.academic_level ?? '—' },
    { label: 'How long have you actively participated in this sport?', value: q.participation_years ?? '—' },
    { label: 'What best describes your current participation level?', value: q.participation_level ?? '—' },
    { label: 'Fitness', value: q.fitness_level != null ? `${q.fitness_level}/5` : '—' },
    { label: 'Technical Skill', value: q.technical_skill != null ? `${q.technical_skill}/5` : '—' },
    { label: 'Leadership', value: q.leadership != null ? `${q.leadership}/5` : '—' },
    { label: 'Data Comfort', value: q.data_comfort != null ? `${q.data_comfort}/5` : '—' },
    { label: 'What is your PRIMARY motivation for participating in sport?', value: q.motivation ?? '—' },
    { label: 'How important is sport to your future career plans?', value: q.career_importance ?? '—' },
    { label: 'Which work environment do you prefer most?', value: q.work_environment ?? '—' },
    { label: 'What is your BIGGEST challenge in pursuing sport seriously?', value: q.biggest_challenge ?? '—' },
    { label: 'Have you experienced any significant sports-related injury in the past 2 years?', value: q.injury_history ?? '—' },
    { label: 'Which THREE sports career paths interest you the most? (Select up to three)', value: q.career_interests?.join(', ') ?? '—' },
  ]
}

function formatRole(role: string): string {
  const labels: Record<string, string> = {
    student: 'Student',
    career_advisor: 'Advisor',
    admin: 'Admin'
  }
  return labels[role] ?? role
}

function roleBadgeClass(role: string): string {
  const map: Record<string, string> = {
    student: 'bg-emerald-50 text-emerald-700 border border-emerald-100',
    career_advisor: 'bg-blue-50 text-blue-700 border border-blue-100',
    admin: 'bg-amber-50 text-amber-700 border border-amber-100'
  }
  return map[role] ?? 'bg-slate-100 text-slate-600'
}

function formatDate(iso: string): string {
  const d = new Date(iso)
  const now = new Date()
  const diffDays = Math.floor((now.getTime() - d.getTime()) / (1000 * 60 * 60 * 24))
  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays}d ago`
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

onMounted(async () => {
  try {
    await Promise.all([
      adminStore.fetchDashboardStats(),
      adminStore.fetchAssessments(10),
      refreshHealth()
    ])
  } catch {
    // Errors stored in adminStore.error
  }
})
</script>
