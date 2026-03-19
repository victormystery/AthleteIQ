import api from './api'
import type { ApiResponse, AuthResponse } from '@/types'
import type { AxiosResponse } from 'axios'

export default {
  login: (credentials: { email: string; password: string }): Promise<AxiosResponse<ApiResponse<AuthResponse>>> =>
    api.post('/auth/login', credentials),
  register: (userData: { name: string; email: string; password: string }): Promise<AxiosResponse<ApiResponse<AuthResponse>>> =>
    api.post('/auth/register', userData),
  logout: (): Promise<AxiosResponse> =>
    api.post('/auth/logout')
}
