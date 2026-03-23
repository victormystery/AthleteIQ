import api from './api'
import type { ApiResponse } from '@/types'
import type { AxiosResponse } from 'axios'

export interface RecommendationItem {
  pathwaySlug: string
  pathwayName: string
  matchPercentage: number
  rank: number
  keySkillsMatch: string[]
  salaryRange?: string
  jobGrowthOutlook?: string
  sportSpecificInsights?: string
}

export interface CareerRecommendation {
  _id: string
  recommendations: RecommendationItem[]
  topRecommendation: string
  motivationRecommendation?: string
  createdAt: string
}

export default {
  getRecommendations: (): Promise<AxiosResponse<ApiResponse<{ recommendations: CareerRecommendation[] }>>> =>
    api.get('/career/recommendations'),

  getHistory: (): Promise<AxiosResponse<ApiResponse<{ history: CareerRecommendation[] }>>> =>
    api.get('/career/history'),
}
