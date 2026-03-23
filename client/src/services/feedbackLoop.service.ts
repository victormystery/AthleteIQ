import api from './api'
import type { ApiResponse } from '@/types'
import type { AxiosResponse } from 'axios'

export interface PathwayInsight {
  pathwaySlug: string
  totalFeedback: number
  averageRating: number
  interestedCount: number
  notInterestedCount: number
  interestedRate: number
}

export interface FeedbackInsights {
  totalSubmissions: number
  totalFeedback: number
  pathwaySummaries: PathwayInsight[]
  topRatedPathway: string
  mostInterestingPathway: string
  averageRatingOverall: number
  generatedAt: string
}

export default {
  getInsights: (): Promise<AxiosResponse<ApiResponse<{ insights: FeedbackInsights }>>> =>
    api.get('/feedback-loop/insights'),
}
