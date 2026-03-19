<template>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <aside
      :class="[
        'w-60 shrink-0 bg-slate-900 text-slate-400 flex flex-col fixed top-0 left-0 h-full z-30',
        'transition-transform duration-300',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
      ]"
    >
      <!-- Brand -->
      <div class="flex items-center gap-3 px-6 py-5 border-b border-white/10">
        <span class="text-primary-400 flex">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-6 h-6">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
        </span>
        <span class="text-base font-bold text-slate-100 tracking-tight">AthleteIQ</span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-3 py-4 overflow-y-auto space-y-0.5">
        <p class="text-[10px] font-bold uppercase tracking-widest text-slate-600 px-3 py-2 mt-1">Main</p>

        <router-link
          to="/app"
          class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors text-slate-400 hover:bg-white/5 hover:text-slate-100"
          exact-active-class="!bg-primary-500/20 !text-primary-300"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4.5 h-4.5">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
          </svg>
          Dashboard
        </router-link>

        <router-link
          to="/app/profile"
          class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors text-slate-400 hover:bg-white/5 hover:text-slate-100"
          active-class="!bg-primary-500/20 !text-primary-300"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4.5 h-4.5">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
          </svg>
          Profile
        </router-link>
      </nav>

      <!-- User footer -->
      <div class="px-3 py-3 border-t border-white/10 flex items-center gap-2">
        <UserAvatar :name="user?.name ?? ''" size="sm" />
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-slate-200 truncate">{{ user?.name ?? 'Athlete' }}</p>
          <p class="text-xs text-slate-500 truncate">{{ user?.email ?? '' }}</p>
        </div>
        <button
          class="shrink-0 text-slate-600 hover:text-red-400 transition-colors p-1.5 rounded-lg hover:bg-white/5"
          title="Logout"
          @click="logout"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </button>
      </div>
    </aside>

    <!-- Overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-black/50 z-20 lg:hidden"
      @click="sidebarOpen = false"
    />

    <!-- Main -->
    <div class="flex flex-col flex-1 min-w-0 lg:ml-60">
      <!-- Topbar -->
      <header class="h-14 bg-white border-b border-slate-200 flex items-center justify-between px-6 sticky top-0 z-10">
        <button
          class="lg:hidden text-slate-500 hover:text-slate-800 p-1.5 rounded-lg transition-colors"
          @click="sidebarOpen = !sidebarOpen"
          aria-label="Toggle menu"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-5 h-5">
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
        <div class="flex items-center gap-3 ml-auto">
          <UserAvatar :name="user?.name ?? ''" size="sm" />
        </div>
      </header>

      <main class="flex-1 p-8 max-w-[1200px] w-full">
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
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStore'
import { useAuth } from '@/composables/useAuth'
import UserAvatar from '@/components/UserAvatar.vue'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)
const { logout } = useAuth()
const sidebarOpen = ref(false)
</script>
