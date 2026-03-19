import mongoose from 'mongoose'
import { QuestionnaireResponse, type IQuestionnaireResponse } from '../models/index.js'
import { careerService } from './career.service.js'
import { googleSheetsService } from './googleSheets.service.js'
import { logger } from '../utils/logger.js'

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
}

export class QuestionnaireService {
  /**
   * Save questionnaire, trigger ML prediction, and export to Google Sheets.
   */
  async submit(userId: mongoose.Types.ObjectId, payload: QuestionnairePayload) {
    // 1. Persist the questionnaire response
    const qResponse = await QuestionnaireResponse.create({
      user: userId,
      ...payload
    })

    // 2. Get ML recommendation
    const recommendation = await careerService.predict(userId, qResponse._id, payload)

    // 3. Export to Google Sheets (non-blocking)
    googleSheetsService.exportSubmission(qResponse, recommendation).catch((err) => {
      logger.warn('Google Sheets export error', { error: (err as Error).message })
    })

    return { questionnaireResponse: qResponse, recommendation }
  }

  /**
   * Get all questionnaire responses for a user.
   */
  async getHistory(userId: mongoose.Types.ObjectId): Promise<IQuestionnaireResponse[]> {
    const docs = await QuestionnaireResponse.find({ user: userId }).sort({ createdAt: -1 }).lean()
    return docs as unknown as IQuestionnaireResponse[]
  }
}

export const questionnaireService = new QuestionnaireService()
