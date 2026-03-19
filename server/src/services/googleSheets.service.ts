import { google } from 'googleapis'
import fs from 'fs'
import path from 'path'
import { env } from '../config/env.js'
import { logger } from '../utils/logger.js'
import type { IQuestionnaireResponse } from '../models/QuestionnaireResponse.model.js'
import type { IPathwayRecommendation } from '../models/PathwayRecommendation.model.js'

export class GoogleSheetsService {
  private isConfigured(): boolean {
    return !!(env.googleSheetsCredentialsPath && env.googleSheetsSpreadsheetId)
  }

  private async getAuthClient() {
    const credPath = path.resolve(env.googleSheetsCredentialsPath!)
    if (!fs.existsSync(credPath)) {
      throw new Error(`Google Sheets credentials file not found at: ${credPath}`)
    }
    const auth = new google.auth.GoogleAuth({
      keyFile: credPath,
      scopes: ['https://www.googleapis.com/auth/spreadsheets']
    })
    return auth.getClient()
  }

  /**
   * Exports a questionnaire submission + its ML results to Google Sheets.
   * Failures are non-blocking and silently logged.
   */
  async exportSubmission(
    questionnaireResponse: IQuestionnaireResponse,
    recommendation: IPathwayRecommendation
  ): Promise<void> {
    if (!this.isConfigured()) {
      logger.debug('Google Sheets export skipped — not configured')
      return
    }

    try {
      const authClient = await this.getAuthClient()
      const sheets = google.sheets({ version: 'v4', auth: authClient as any })

      const topRec = recommendation.recommendations[0]
      const row = [
        new Date().toISOString(),
        String(questionnaireResponse.user),
        questionnaireResponse.academic_level,
        questionnaireResponse.primary_sport,
        questionnaireResponse.participation_years,
        questionnaireResponse.participation_level,
        questionnaireResponse.fitness_level,
        questionnaireResponse.technical_skill,
        questionnaireResponse.leadership,
        questionnaireResponse.data_comfort,
        questionnaireResponse.motivation,
        questionnaireResponse.career_importance,
        questionnaireResponse.work_environment,
        questionnaireResponse.biggest_challenge,
        questionnaireResponse.injury_history,
        questionnaireResponse.career_interests.join(', '),
        // ML predictions
        topRec?.pathwayName ?? '',
        topRec?.matchPercentage ?? '',
        recommendation.recommendations
          .map((r) => `${r.pathwayName}(${r.matchPercentage}%)`)
          .join(' | '),
        recommendation.motivationRecommendation?.pathwayName ?? ''
      ]

      await sheets.spreadsheets.values.append({
        spreadsheetId: env.googleSheetsSpreadsheetId!,
        range: 'Sheet1!A1',
        valueInputOption: 'RAW',
        requestBody: { values: [row] }
      })

      logger.info('Questionnaire exported to Google Sheets successfully')
    } catch (err) {
      // Export failures are non-blocking
      logger.warn('Google Sheets export failed (non-blocking)', { error: (err as Error).message })
    }
  }

  /**
   * Ensures the header row exists in the spreadsheet.
   */
  async ensureHeaders(): Promise<void> {
    if (!this.isConfigured()) return

    try {
      const authClient = await this.getAuthClient()
      const sheets = google.sheets({ version: 'v4', auth: authClient as any })

      const res = await sheets.spreadsheets.values.get({
        spreadsheetId: env.googleSheetsSpreadsheetId!,
        range: 'Sheet1!A1:T1'
      })

      if (!res.data.values || res.data.values.length === 0) {
        const headers = [
          'Timestamp',
          'User ID',
          'Academic Level',
          'Primary Sport',
          'Participation Years',
          'Participation Level',
          'Fitness Level',
          'Technical Skill',
          'Leadership',
          'Data Comfort',
          'Motivation',
          'Career Importance',
          'Work Environment',
          'Biggest Challenge',
          'Injury History',
          'Career Interests',
          'Top Recommendation',
          'Top Match %',
          'All Recommendations',
          'Motivation Recommendation'
        ]
        await sheets.spreadsheets.values.update({
          spreadsheetId: env.googleSheetsSpreadsheetId!,
          range: 'Sheet1!A1',
          valueInputOption: 'RAW',
          requestBody: { values: [headers] }
        })
        logger.info('Google Sheets headers initialised')
      }
    } catch (err) {
      logger.warn('Failed to initialise Google Sheets headers (non-blocking)', {
        error: (err as Error).message
      })
    }
  }
}

export const googleSheetsService = new GoogleSheetsService()
