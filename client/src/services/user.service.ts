import api from './api'
import type { ApiResponse, User } from '@/types'
import type { AxiosResponse } from 'axios'

export default {
  getProfile: (): Promise<AxiosResponse<ApiResponse<User>>> =>
    api.get('/users/me'),
  updateProfile: (data: Partial<Pick<User, 'name'>>): Promise<AxiosResponse<ApiResponse<User>>> =>
    api.put('/users/me', data)
}
