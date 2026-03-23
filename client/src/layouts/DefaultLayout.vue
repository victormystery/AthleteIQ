<template>
  <div class="flex min-h-screen bg-slate-50">
    <!-- Sidebar -->
    <aside
      :class="[
        'w-64 shrink-0 bg-[#0c1220] flex flex-col fixed top-0 left-0 h-full z-30',
        'transition-transform duration-300 ease-in-out',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      ]"
    >
      <!-- Brand -->
      <div class="flex items-center h-16 px-5 border-b border-white/5 shrink-0">
        <img src="/athleteiqLogo.svg" alt="AthleteIQ" class="h-7 w-auto" style="filter: brightness(0) invert(1);" />
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-3 py-5 overflow-y-auto">
        <!-- Main section -->
        <div class="mb-6">
          <p class="text-[10px] font-bold uppercase tracking-widest text-slate-600 px-3 mb-2">Main</p>
          <div class="space-y-0.5">
            <router-link
              to="/app"
              class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 text-slate-400 hover:bg-white/5 hover:text-slate-100 border-l-2 border-transparent"
              exact-active-class="!bg-primary-500/10 !text-primary-300 !border-l-primary-500"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" class="shrink-0">
                <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>
                <rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>
              </svg>
              Dashboard
            </router-link>

            <router-link
              to="/app/profile"
              class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 text-slate-400 hover:bg-white/5 hover:text-slate-100 border-l-2 border-transparent"
              active-class="!bg-primary-500/10 !text-primary-300 !border-l-primary-500"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" class="shrink-0">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
              </svg>
              Profile
            </router-link>
          </div>
        </div>

        <!-- Admin section — only visible to admins -->
        <template v-if="isAdmin">
          <div>
            <p class="text-[10px] font-bold uppercase tracking-widest text-slate-600 px-3 mb-2">Administration</p>
            <div class="space-y-0.5">
              <router-link
                to="/admin"
                class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 text-slate-400 hover:bg-white/5 hover:text-slate-100 border-l-2 border-transparent"
                exact-active-class="!bg-primary-500/10 !text-primary-300 !border-l-primary-500"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" class="shrink-0">
                  <path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-4"/>
                </svg>
                Overview
              </router-link>

              <router-link
                to="/admin/users"
                class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 text-slate-400 hover:bg-white/5 hover:text-slate-100 border-l-2 border-transparent"
                active-class="!bg-primary-500/10 !text-primary-300 !border-l-primary-500"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" class="shrink-0">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
                User Management
              </router-link>
            </div>
          </div>
        </template>
      </nav>

      <!-- User footer -->
      <div class="px-3 py-4 border-t border-white/5 shrink-0">
        <div class="flex items-center gap-3 px-2 py-2 rounded-xl hover:bg-white/5 transition-colors">
          <UserAvatar :name="user?.name ?? ''" size="sm" />
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-slate-100 truncate leading-tight">{{ user?.name ?? 'Athlete' }}</p>
            <p class="text-xs text-slate-500 truncate mt-0.5">{{ roleLabel }}</p>
          </div>
          <button
            class="shrink-0 p-1.5 rounded-lg text-slate-600 hover:text-red-400 hover:bg-white/5 transition-colors"
            title="Sign out"
            @click="logout"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-black/60 backdrop-blur-sm z-20 lg:hidden"
      @click="sidebarOpen = false"
    />

    <!-- Main content -->
    <div class="flex flex-col flex-1 min-w-0 lg:ml-64">
      <!-- Topbar -->
      <header class="h-16 bg-white/80 backdrop-blur-sm border-b border-slate-200/80 flex items-center gap-4 px-6 sticky top-0 z-10">
        <!-- Mobile hamburger -->
        <button
          class="lg:hidden -ml-1 p-2 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition-colors"
          aria-label="Toggle menu"
          @click="sidebarOpen = !sidebarOpen"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-5 h-5">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>

        <!-- Page title -->
        <div class="flex-1 min-w-0">
          <h1 class="text-base font-semibold text-slate-800 truncate">{{ currentPageTitle }}</h1>
        </div>

        <!-- Right side -->
        <div class="flex items-center gap-2 shrink-0">
          <!-- Notification bell -->
          <button class="relative p-2 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-5 h-5">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
          </button>

          <!-- Divider -->
          <div class="w-px h-6 bg-slate-200 mx-1" />

          <!-- User info -->
          <div class="flex items-center gap-2.5">
            <UserAvatar :name="user?.name ?? ''" size="sm" />
            <div class="hidden sm:block text-right leading-tight">
              <p class="text-sm font-semibold text-slate-800">{{ user?.name?.split(' ')[0] ?? 'Athlete' }}</p>
              <p class="text-xs text-slate-400">{{ roleLabel }}</p>
            </div>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 p-6 lg:p-8 w-full max-w-[1280px]">
        <router-view v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStore'
import { useAuth } from '@/composables/useAuth'
import UserAvatar from '@/components/UserAvatar.vue'

const authStore = useAuthStore()
const { user, isAdmin } = storeToRefs(authStore)
const { logout } = useAuth()
const route = useRoute()

const sidebarOpen = ref(false)

const roleLabel = computed(() => {
  const map: Record<string, string> = {
    student: 'Student',
    career_advisor: 'Career Advisor',
    admin: 'Administrator'
  }
  return map[user.value?.role ?? ''] ?? 'Member'
})

const currentPageTitle = computed(() => {
  const map: Record<string, string> = {
    Dashboard: 'Dashboard',
    Profile: 'My Profile',
    AdminDashboard: 'Admin Overview',
    AdminUsers: 'User Management'
  }
  return map[route.name as string] ?? 'AthleteIQ'
})
</script>
