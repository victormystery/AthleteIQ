import api from './api'
import type { ApiResponse } from '@/types'
import type { AxiosResponse } from 'axios'

export interface RoadmapSummaryItem {
  pathwaySlug: string
  pathwayTitle: string
  overallProgress: number
  lastActivityAt: string
}

export default {
  getSummary: (): Promise<AxiosResponse<ApiResponse<{ summary: RoadmapSummaryItem[] }>>> =>
    api.get('/roadmap/summary'),
}
