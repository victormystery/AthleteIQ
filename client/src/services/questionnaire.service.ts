import api from './api'
import type { ApiResponse } from '@/types'
import type { AxiosResponse } from 'axios'
import type { CareerRecommendation } from './career.service'

export interface QuestionnairePayload {
  academic_level: string
  primary_sport: string
  participation_years: string
  participation_level: string
  fitness_level: number
  technical_skill: number
  leadership: number
  data_comfort: number
  motivation: string
  career_importance: string
  work_environment: string
  biggest_challenge: string
  injury_history: string
  career_interests: string[]
  education_training_level: string
}

export interface QuestionnaireResponse {
  _id: string
  academic_level: string
  primary_sport: string
  participation_years: string
  participation_level: string
  fitness_level: number
  technical_skill: number
  leadership: number
  data_comfort: number
  motivation: string
  career_importance: string
  work_environment: string
  biggest_challenge: string
  injury_history: string
  career_interests: string[]
  education_training_level: string
  createdAt: string
}

export interface SubmitResult {
  questionnaireResponse: QuestionnaireResponse
  recommendation: CareerRecommendation
}

export default {
  submit: (payload: QuestionnairePayload): Promise<AxiosResponse<ApiResponse<SubmitResult>>> =>
    api.post('/questionnaire', payload),

  getHistory: (): Promise<AxiosResponse<ApiResponse<{ responses: QuestionnaireResponse[] }>>> =>
    api.get('/questionnaire/my'),
}
