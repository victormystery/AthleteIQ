<template>
  <div>
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-2xl font-bold text-slate-800">User Management</h1>
        <p class="text-sm text-slate-500 mt-0.5">
          <span v-if="pagination">{{ pagination.total }} total users registered</span>
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

    <!-- Error State -->
    <BaseAlert v-if="error" type="error" :show="!!error" dismissible @dismiss="error = null" class="mb-6">
      {{ error }}
    </BaseAlert>

    <!-- Filter Bar -->
    <div class="flex flex-col sm:flex-row gap-3 mb-5">
      <!-- Search -->
      <div class="relative flex-1 max-w-sm">
        <div class="absolute inset-y-0 left-3 flex items-center pointer-events-none">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-4 h-4 text-slate-400">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
        </div>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by name or email…"
          class="w-full pl-9 pr-3 py-2 text-sm border border-slate-200 rounded-lg bg-white text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-400 transition-colors"
        />
      </div>

      <!-- Role filter pills -->
      <div class="flex items-center gap-2 flex-wrap">
        <button
          v-for="f in roleFilters"
          :key="f.value"
          :class="[
            'px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all duration-150',
            roleFilter === f.value
              ? 'bg-primary-600 text-white border-primary-600 shadow-sm'
              : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300 hover:bg-slate-50'
          ]"
          @click="roleFilter = f.value"
        >
          {{ f.label }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && users.length === 0" class="flex items-center justify-center py-24">
      <AppSpinner size="lg" />
    </div>

    <!-- Table Card -->
    <BaseCard v-else>
      <!-- Empty state -->
      <div v-if="filteredUsers.length === 0" class="text-center py-16">
        <div class="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-3">
          <svg viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" class="w-6 h-6">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
          </svg>
        </div>
        <p class="text-sm font-semibold text-slate-600">No users found</p>
        <p class="text-xs text-slate-400 mt-1">Try adjusting your search or filter.</p>
        <button
          v-if="searchQuery || roleFilter !== 'all'"
          class="text-xs text-primary-600 font-semibold hover:text-primary-700 mt-3 transition-colors"
          @click="clearFilters"
        >
          Clear filters
        </button>
      </div>

      <div v-else class="overflow-x-auto -mx-6 -my-6">
        <table class="w-full">
          <thead>
            <tr class="bg-slate-50/80 border-b border-slate-200">
              <th class="text-left text-[11px] font-bold text-slate-500 uppercase tracking-wider px-6 py-3.5">User</th>
              <th class="text-left text-[11px] font-bold text-slate-500 uppercase tracking-wider px-6 py-3.5">Role</th>
              <th class="text-left text-[11px] font-bold text-slate-500 uppercase tracking-wider px-6 py-3.5 hidden sm:table-cell">Joined</th>
              <th class="text-right text-[11px] font-bold text-slate-500 uppercase tracking-wider px-6 py-3.5">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr
              v-for="u in filteredUsers"
              :key="u._id"
              class="group hover:bg-slate-50/80 transition-colors"
            >
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="relative shrink-0">
                    <UserAvatar :name="u.name" size="sm" />
                    <div
                      v-if="u.suspended"
                      class="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-red-500 rounded-full border-2 border-white"
                      title="Suspended"
                    />
                  </div>
                  <div class="min-w-0">
                    <div class="flex items-center gap-2">
                      <p class="text-sm font-semibold text-slate-800 truncate">{{ u.name }}</p>
                      <span
                        v-if="u.suspended"
                        class="shrink-0 text-[10px] px-1.5 py-0.5 rounded-md font-semibold bg-red-100 text-red-600 border border-red-200"
                      >Suspended</span>
                    </div>
                    <p class="text-xs text-slate-400 truncate mt-0.5">{{ u.email }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span
                  :class="roleBadgeClass(u.role)"
                  class="text-[11px] px-2.5 py-1 rounded-full font-semibold border"
                >
                  {{ formatRole(u.role) }}
                </span>
              </td>
              <td class="px-6 py-4 hidden sm:table-cell">
                <span class="text-sm text-slate-500">{{ formatDate(u.createdAt) }}</span>
              </td>
              <td class="px-6 py-4 text-right">
                <template v-if="u.role !== 'admin'">
                  <BaseButton
                    tag="button"
                    variant="ghost"
                    size="sm"
                    :disabled="!!deleting || !!updatingRole || !!suspending"
                    class="mr-1"
                    @click="openRoleModal(u)"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5">
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                      <circle cx="9" cy="7" r="4"/>
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                    </svg>
                    Role
                  </BaseButton>
                  <BaseButton
                    tag="button"
                    :variant="u.suspended ? 'outline' : 'ghost'"
                    size="sm"
                    :loading="suspending === u._id"
                    :disabled="!!deleting || !!updatingRole || !!suspending"
                    class="mr-1"
                    @click="handleSuspend(u)"
                  >
                    <svg v-if="u.suspended" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5">
                      <path d="M9 12l2 2 4-4"/>
                      <circle cx="12" cy="12" r="10"/>
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="w-3.5 h-3.5">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                    </svg>
                    {{ u.suspended ? 'Unsuspend' : 'Suspend' }}
                  </BaseButton>
                  <BaseButton
                    tag="button"
                    variant="danger"
                    size="sm"
                    :loading="deleting === u._id"
                    :disabled="!!deleting || !!updatingRole || !!suspending"
                    @click="confirmDelete(u)"
                  >
                    <svg viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5">
                      <path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.519.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5zM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4zM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5z" clip-rule="evenodd"/>
                    </svg>
                    Delete
                  </BaseButton>
                </template>
                <span v-else class="text-xs text-slate-400 italic font-medium">Protected</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <template v-if="pagination && pagination.pages > 1" #footer>
        <div class="flex items-center justify-between w-full">
          <p class="text-sm text-slate-500">
            Showing page <span class="font-semibold text-slate-700">{{ pagination.page }}</span>
            of <span class="font-semibold text-slate-700">{{ pagination.pages }}</span>
            <span class="text-slate-400 ml-1">({{ pagination.total }} total)</span>
          </p>
          <div class="flex items-center gap-2">
            <BaseButton
              tag="button"
              variant="secondary"
              size="sm"
              :disabled="pagination.page <= 1 || loading"
              @click="changePage(pagination.page - 1)"
            >
              <svg viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4">
                <path fill-rule="evenodd" d="M17 10a.75.75 0 0 1-.75.75H5.612l4.158 3.96a.75.75 0 1 1-1.04 1.08l-5.5-5.25a.75.75 0 0 1 0-1.08l5.5-5.25a.75.75 0 1 1 1.04 1.08L5.612 9.25H16.25A.75.75 0 0 1 17 10z" clip-rule="evenodd"/>
              </svg>
              Previous
            </BaseButton>
            <BaseButton
              tag="button"
              variant="secondary"
              size="sm"
              :disabled="pagination.page >= pagination.pages || loading"
              @click="changePage(pagination.page + 1)"
            >
              Next
              <svg viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4">
                <path fill-rule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10z" clip-rule="evenodd"/>
              </svg>
            </BaseButton>
          </div>
        </div>
      </template>
    </BaseCard>

    <!-- Delete Confirmation Modal -->
    <BaseModal v-model="showDeleteModal" title="Delete User">
      <div class="flex items-start gap-3">
        <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center shrink-0">
          <svg viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2" class="w-5 h-5">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </div>
        <div>
          <p class="text-sm font-semibold text-slate-800">Are you absolutely sure?</p>
          <p class="text-sm text-slate-600 mt-1">
            You are about to permanently delete
            <strong class="font-semibold text-slate-800">{{ userToDelete?.name }}</strong>.
            This action cannot be undone.
          </p>
        </div>
      </div>
      <template #footer>
        <BaseButton tag="button" variant="secondary" @click="showDeleteModal = false">Cancel</BaseButton>
        <BaseButton tag="button" variant="danger" :loading="!!deleting" @click="handleDelete">Delete User</BaseButton>
      </template>
    </BaseModal>

    <!-- Role Change Modal -->
    <BaseModal v-model="showRoleModal" title="Change User Role">
      <div class="flex flex-col gap-4">
        <div class="flex items-center gap-3">
          <UserAvatar :name="roleChangeUser?.name ?? ''" size="sm" />
          <div>
            <p class="text-sm font-semibold text-slate-800">{{ roleChangeUser?.name }}</p>
            <p class="text-xs text-slate-500">{{ roleChangeUser?.email }}</p>
          </div>
        </div>
        <div>
          <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">Select new role</p>
          <div class="flex gap-2">
            <button
              v-for="r in changeableRoles" :key="r.value"
              type="button"
              :class="[
                'flex-1 py-2.5 px-3 rounded-xl border text-sm font-semibold transition-all',
                selectedRole === r.value
                  ? 'border-primary-500 bg-primary-50 text-primary-700'
                  : 'border-slate-200 text-slate-600 hover:border-slate-300'
              ]"
              @click="selectedRole = r.value as 'student' | 'career_advisor'"
            >{{ r.label }}</button>
          </div>
        </div>
        <p v-if="roleChangeUser && selectedRole === roleChangeUser.role" class="text-xs text-slate-400">
          This user already has this role.
        </p>
      </div>
      <template #footer>
        <BaseButton tag="button" variant="secondary" @click="showRoleModal = false">Cancel</BaseButton>
        <BaseButton
          tag="button"
          :loading="!!updatingRole"
          :disabled="!selectedRole || selectedRole === roleChangeUser?.role"
          @click="handleRoleChange"
        >
          Update Role
        </BaseButton>
      </template>
    </BaseModal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAdminStore } from '@/stores/adminStore'
import { useToast } from '@/composables/useToast'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseModal from '@/components/BaseModal.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import AppSpinner from '@/components/AppSpinner.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import type { User } from '@/types'

const adminStore = useAdminStore()
const toast = useToast()
const { users, pagination, loading, error } = storeToRefs(adminStore)

const showDeleteModal = ref(false)
const userToDelete = ref<User | null>(null)
const deleting = ref<string | null>(null)
const suspending = ref<string | null>(null)
const searchQuery = ref('')
const roleFilter = ref<'all' | 'student' | 'career_advisor' | 'admin'>('all')

const showRoleModal = ref(false)
const roleChangeUser = ref<User | null>(null)
const selectedRole = ref<'student' | 'career_advisor'>('student')
const updatingRole = ref<string | null>(null)

const changeableRoles = [
  { value: 'student', label: 'Student' },
  { value: 'career_advisor', label: 'Career Advisor' }
]

const roleFilters = [
  { label: 'All', value: 'all' as const },
  { label: 'Students', value: 'student' as const },
  { label: 'Advisors', value: 'career_advisor' as const },
  { label: 'Admins', value: 'admin' as const }
]

const filteredUsers = computed(() => {
  let result = users.value
  if (roleFilter.value !== 'all') {
    result = result.filter(u => u.role === roleFilter.value)
  }
  const q = searchQuery.value.trim().toLowerCase()
  if (q) {
    result = result.filter(u =>
      u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q)
    )
  }
  return result
})

function clearFilters() {
  searchQuery.value = ''
  roleFilter.value = 'all'
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
    student: 'bg-emerald-50 text-emerald-700 border-emerald-100',
    career_advisor: 'bg-blue-50 text-blue-700 border-blue-100',
    admin: 'bg-amber-50 text-amber-700 border-amber-100'
  }
  return map[role] ?? 'bg-slate-100 text-slate-600 border-slate-200'
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric'
  })
}

function confirmDelete(user: User) {
  userToDelete.value = user
  showDeleteModal.value = true
}

async function handleDelete() {
  if (!userToDelete.value) return
  deleting.value = userToDelete.value._id
  try {
    await adminStore.deleteUser(userToDelete.value._id)
    toast.success(`"${userToDelete.value.name}" has been removed.`)
    showDeleteModal.value = false
  } catch {
    toast.error('Failed to delete user. Please try again.')
  } finally {
    deleting.value = null
    userToDelete.value = null
  }
}

async function handleSuspend(user: User) {
  suspending.value = user._id
  const isSuspended = !!user.suspended
  try {
    await adminStore.suspendUser(user._id, !isSuspended)
    toast.success(isSuspended ? `${user.name} has been unsuspended.` : `${user.name} has been suspended.`)
  } catch {
    toast.error('Failed to update suspension status. Please try again.')
  } finally {
    suspending.value = null
  }
}

function openRoleModal(user: User) {
  roleChangeUser.value = user
  selectedRole.value = user.role as 'student' | 'career_advisor'
  showRoleModal.value = true
}

async function handleRoleChange() {
  if (!roleChangeUser.value || !selectedRole.value) return
  updatingRole.value = roleChangeUser.value._id
  try {
    await adminStore.updateUserRole(roleChangeUser.value._id, selectedRole.value)
    toast.success(`${roleChangeUser.value.name}'s role updated to ${selectedRole.value === 'career_advisor' ? 'Career Advisor' : 'Student'}.`)
    showRoleModal.value = false
  } catch {
    toast.error('Failed to update role. Please try again.')
  } finally {
    updatingRole.value = null
    roleChangeUser.value = null
  }
}

async function changePage(page: number) {
  try {
    await adminStore.fetchUsers(page)
  } catch {
    // Error is stored in the store
  }
}

onMounted(async () => {
  try {
    await adminStore.fetchUsers()
  } catch {
    // Error is stored in the store
  }
})
</script>
