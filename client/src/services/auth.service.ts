import api from './api'
import type { ApiResponse, AuthResponse, RegisterResponse } from '@/types'
import type { AxiosResponse } from 'axios'

export default {
  login: (credentials: { email: string; password: string }): Promise<AxiosResponse<ApiResponse<AuthResponse>>> =>
    api.post('/auth/login', credentials),
  register: (userData: { name: string; email: string; password: string }): Promise<AxiosResponse<ApiResponse<RegisterResponse>>> =>
    api.post('/auth/register', userData),
  exchangeGoogleCode: (code: string): Promise<AxiosResponse<ApiResponse<AuthResponse>>> =>
    api.post('/auth/google/exchange', { code }),
  logout: (): Promise<AxiosResponse> =>
    api.post('/auth/logout')
}
