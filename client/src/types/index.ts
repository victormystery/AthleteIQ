export interface User {
  _id: string
  name: string
  email: string
  role: 'athlete' | 'coach' | 'admin'
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
