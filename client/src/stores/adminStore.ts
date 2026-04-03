import { defineStore } from 'pinia'
import { ref } from 'vue'
import adminService from '@/services/admin.service'
import type {
  AdminStats,
  User,
  PaginationMeta,
  Assessment
} from '@/types'

export const useAdminStore = defineStore('admin', () => {
  // ── State ────────────────────────────────────────────────────────────────
  const stats = ref<AdminStats | null>(null)
  const recentUsers = ref<User[]>([])
  const users = ref<User[]>([])
  const pagination = ref<PaginationMeta | null>(null)
  const assessments = ref<Assessment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // ── Helpers ──────────────────────────────────────────────────────────────
  function extractError(err: unknown): string {
    const e = err as { response?: { data?: { message?: string } }; message?: string }
    return e.response?.data?.message ?? e.message ?? 'An unexpected error occurred'
  }

  // ── Actions ──────────────────────────────────────────────────────────────

  async function fetchDashboardStats(): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const { data } = await adminService.getDashboardStats()
      stats.value = data.data.stats
      recentUsers.value = data.data.recentUsers
    } catch (err) {
      error.value = extractError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchUsers(page = 1, limit = 20): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const { data } = await adminService.listUsers(page, limit)
      users.value = data.data.users
      pagination.value = data.data.pagination
    } catch (err) {
      error.value = extractError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchAssessments(limit = 20): Promise<void> {
    loading.value = true
    error.value = null
    try {
      const { data } = await adminService.getRecentAssessments(limit)
      assessments.value = data.data.assessments
    } catch (err) {
      error.value = extractError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteUser(id: string): Promise<void> {
    error.value = null
    try {
      await adminService.deleteUser(id)
      // Optimistic removal from local list
      users.value = users.value.filter(u => u._id !== id)
      recentUsers.value = recentUsers.value.filter(u => u._id !== id)
      // Decrement total if pagination is available
      if (pagination.value) {
        pagination.value.total -= 1
        pagination.value.pages = Math.ceil(pagination.value.total / pagination.value.limit)
      }
    } catch (err) {
      error.value = extractError(err)
      throw err
    }
  }

  async function suspendUser(id: string, suspended: boolean): Promise<void> {
    error.value = null
    try {
      const { data } = await adminService.suspendUser(id, suspended)
      const updated = (data.data as { user: User }).user as User
      const updateInList = (list: User[]) => {
        const idx = list.findIndex(u => u._id === id)
        if (idx > -1) list[idx] = { ...list[idx], suspended: updated.suspended }
      }
      updateInList(users.value)
      updateInList(recentUsers.value)
    } catch (err) {
      error.value = extractError(err)
      throw err
    }
  }

  async function updateUserRole(id: string, role: 'student' | 'career_advisor'): Promise<void> {
    error.value = null
    try {
      const { data } = await adminService.updateUserRole(id, role)
      const updated = (data.data as { user: User }).user as User
      // Update in both lists optimistically
      const updateInList = (list: User[]) => {
        const idx = list.findIndex(u => u._id === id)
        if (idx > -1) list[idx] = { ...list[idx], role: updated.role }
      }
      updateInList(users.value)
      updateInList(recentUsers.value)
    } catch (err) {
      error.value = extractError(err)
      throw err
    }
  }

  function $reset() {
    stats.value = null
    recentUsers.value = []
    users.value = []
    pagination.value = null
    assessments.value = []
    loading.value = false
    error.value = null
  }

  return {
    // state
    stats,
    recentUsers,
    users,
    pagination,
    assessments,
    loading,
    error,
    // actions
    fetchDashboardStats,
    fetchUsers,
    fetchAssessments,
    deleteUser,
    suspendUser,
    updateUserRole,
    $reset
  }
})
