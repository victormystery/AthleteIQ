import axios from 'axios'
import api from './api'
import type {
  ApiResponse,
  AdminDashboardData,
  PaginatedUsers,
  AssessmentsData,
  SystemHealth
} from '@/types'
import type { AxiosResponse } from 'axios'

// Derive root server URL by stripping trailing /api from the API base URL
const serverRoot = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/api\/?$/, '') || ''
const systemApi = axios.create({ baseURL: serverRoot, timeout: 5000 })

export default {
  /** GET /api/admin/stats — dashboard overview */
  getDashboardStats: (): Promise<AxiosResponse<ApiResponse<AdminDashboardData>>> =>
    api.get('/admin/stats'),

  /** GET /api/admin/users?page=&limit= — paginated user list */
  listUsers: (
    page = 1,
    limit = 20
  ): Promise<AxiosResponse<ApiResponse<PaginatedUsers>>> =>
    api.get('/admin/users', { params: { page, limit } }),

  /** GET /api/admin/assessments?limit= — recent assessments */
  getRecentAssessments: (
    limit = 20
  ): Promise<AxiosResponse<ApiResponse<AssessmentsData>>> =>
    api.get('/admin/assessments', { params: { limit } }),

  /** DELETE /api/admin/users/:id — remove a user */
  deleteUser: (id: string): Promise<AxiosResponse<ApiResponse<null>>> =>
    api.delete(`/admin/users/${id}`),

  /** PATCH /api/admin/users/:id/suspend — suspend or unsuspend a user */
  suspendUser: (
    id: string,
    suspended: boolean
  ): Promise<AxiosResponse<ApiResponse<{ user: unknown }>>> =>
    api.patch(`/admin/users/${id}/suspend`, { suspended }),

  /** PATCH /api/admin/users/:id/role — change a user's role */
  updateUserRole: (
    id: string,
    role: 'student' | 'career_advisor'
  ): Promise<AxiosResponse<ApiResponse<{ user: unknown }>>> =>
    api.patch(`/admin/users/${id}/role`, { role }),

  /** GET /health — server + DB + ML health check (no auth required) */
  getSystemHealth: (): Promise<AxiosResponse<SystemHealth>> =>
    systemApi.get('/health')
}
