<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-slate-800">Dashboard</h1>
      <p class="mt-1 text-sm text-slate-500">
        Welcome back, <strong class="font-semibold text-slate-700">{{ user?.name ?? 'Athlete' }}</strong>. Here's your overview.
      </p>
    </div>

    <!-- Stats grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <StatCard label="Workouts this week" value="6" :change="20" icon-bg="#ffedd5">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2" class="w-5.5 h-5.5"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
        </template>
      </StatCard>
      <StatCard label="Total distance (km)" value="42.5" :change="8" icon-bg="#dcfce7">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" class="w-5.5 h-5.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        </template>
      </StatCard>
      <StatCard label="Avg. heart rate" value="142 bpm" :change="-3" icon-bg="#fee2e2">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2" class="w-5.5 h-5.5"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
        </template>
      </StatCard>
      <StatCard label="Personal records" value="3" :change="50" icon-bg="#fef3c7">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2" class="w-5.5 h-5.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        </template>
      </StatCard>
    </div>

    <!-- Content -->
    <div class="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-6">
      <BaseCard title="Recent Activity" subtitle="Your last 5 sessions">
        <ul class="divide-y divide-slate-100">
          <li v-for="item in recentActivity" :key="item.id" class="flex items-center gap-3 py-3 first:pt-0 last:pb-0">
            <div class="w-9 h-9 rounded-lg flex items-center justify-center text-base shrink-0" :style="{ background: item.bg }">
              {{ item.emoji }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-slate-800">{{ item.name }}</p>
              <p class="text-xs text-slate-400 mt-0.5">{{ item.date }} · {{ item.duration }}</p>
            </div>
            <span class="text-xs bg-primary-50 text-primary-700 px-2.5 py-0.5 rounded-full font-medium whitespace-nowrap">
              {{ item.type }}
            </span>
          </li>
        </ul>
      </BaseCard>

      <BaseCard title="Quick Actions">
        <div class="flex flex-col gap-3">
          <BaseButton variant="outline" :block="true" @click="showLogModal = true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Log Workout
          </BaseButton>
          <BaseButton variant="secondary" :block="true" @click="toast.info('Analytics coming soon!')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4"><path d="M18 20V10"/><path d="M12 20V4"/><path d="M6 20v-6"/></svg>
            View Analytics
          </BaseButton>
          <BaseButton variant="secondary" :block="true" @click="toast.info('Scheduling coming soon!')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            Schedule Session
          </BaseButton>
        </div>
      </BaseCard>
    </div>

    <!-- Log workout modal -->
    <BaseModal v-model="showLogModal" title="Log Workout">
      <div class="flex flex-col gap-4">
        <BaseInput v-model="newWorkout.type" label="Workout type" placeholder="e.g. Running, Cycling…" />
        <BaseInput v-model="newWorkout.duration" label="Duration (minutes)" type="number" placeholder="45" />
        <BaseInput v-model="newWorkout.notes" label="Notes" placeholder="How did it go?" />
      </div>
      <template #footer>
        <BaseButton variant="secondary" @click="showLogModal = false">Cancel</BaseButton>
        <BaseButton @click="logWorkout">Save workout</BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStore'
import { useToast } from '@/composables/useToast'
import StatCard from '@/components/StatCard.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseModal from '@/components/BaseModal.vue'
import BaseInput from '@/components/BaseInput.vue'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)
const toast = useToast()

const showLogModal = ref(false)
const newWorkout = reactive({ type: '', duration: '', notes: '' })

const recentActivity = [
  { id: 1, name: 'Morning Run',       date: 'Today',     duration: '42 min',  type: 'Cardio',    emoji: '🏃', bg: '#ede9fe' },
  { id: 2, name: 'Cycling',           date: 'Yesterday', duration: '1h 15m',  type: 'Endurance', emoji: '🚴', bg: '#dcfce7' },
  { id: 3, name: 'Strength Training', date: 'Mar 17',    duration: '55 min',  type: 'Strength',  emoji: '🏋️', bg: '#fef3c7' },
  { id: 4, name: 'Swimming',          date: 'Mar 16',    duration: '30 min',  type: 'Cardio',    emoji: '🏊', bg: '#ffedd5' },
  { id: 5, name: 'Yoga',             date: 'Mar 15',    duration: '45 min',  type: 'Recovery',  emoji: '🧘', bg: '#fce7f3' }
]

function logWorkout() {
  if (!newWorkout.type) {
    toast.error('Please enter a workout type')
    return
  }
  toast.success(`"${newWorkout.type}" logged successfully!`)
  showLogModal.value = false
  Object.assign(newWorkout, { type: '', duration: '', notes: '' })
}
</script>
