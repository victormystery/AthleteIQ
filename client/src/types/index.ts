export interface User {
  _id: string
  name: string
  email: string
  role: 'student' | 'career_advisor' | 'admin'
  suspended?: boolean
  createdAt: string
  updatedAt: string
}

export interface AuthResponse {
  token: string
  user: User
}

export interface RegisterResponse {
  user: User
}

export interface ApiResponse<T = unknown> {
  success: boolean
  message: string
  data: T
}

export interface Toast {
  id: number
  type: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
}

export interface WorkoutLog {
  type: string
  duration: string
  notes: string
}

// ── Admin types ──────────────────────────────────────────────────────────────

export interface AdminStats {
  totalUsers: number
  totalStudents: number
  totalAdvisors: number
  totalAssessments: number
  totalFeedback: number
}

export interface AdminDashboardData {
  stats: AdminStats
  recentUsers: User[]
}

export interface PaginationMeta {
  page: number
  limit: number
  total: number
  pages: number
}

export interface PaginatedUsers {
  users: User[]
  pagination: PaginationMeta
}

export interface QuestionnaireResponseData {
  _id?: string
  primary_sport?: string
  academic_level?: string
  participation_years?: string
  participation_level?: string
  fitness_level?: number
  technical_skill?: number
  leadership?: number
  data_comfort?: number
  motivation?: string
  career_importance?: string
  work_environment?: string
  biggest_challenge?: string
  injury_history?: string
  career_interests?: string[]
  education_training_level?: string
  createdAt?: string
}

export interface Assessment {
  _id: string
  user: Pick<User, '_id' | 'name' | 'email' | 'role'> | null
  questionnaireResponse: QuestionnaireResponseData | null
  topRecommendation?: string
  createdAt: string
}

export interface AssessmentsData {
  assessments: Assessment[]
}

export interface SystemHealth {
  status: 'ok' | 'error'
  env: string
  timestamp: string
}
