// cspell:ignore googleusercontent
import { google } from 'googleapis'
import fs from 'fs'
import path from 'path'
import { env } from '../config/env.js'
import { logger } from '../utils/logger.js'
import type { IQuestionnaireResponse } from '../models/QuestionnaireResponse.model.js'
import type { IPathwayRecommendation } from '../models/PathwayRecommendation.model.js'

type SheetsClient = ReturnType<typeof google.sheets>

// Google OAuth Client IDs follow the pattern:
//   <project-number>-<random>.apps.googleusercontent.com
// We match partial/truncated variants (.co, .c, etc.) since the full suffix is irrelevant.
const OAUTH_CLIENT_ID_RE = /\d{6,}-[a-z0-9]+\.apps\.googleusercontent/i

export class GoogleSheetsService {
  private worksheetNameCache: string | null = null
  private spreadsheetIdCache: string | null = null

  private hasAuthSourceConfigured(): boolean {
    return Boolean(
      env.googleSheetsCredentialsJson ||
        env.googleSheetsCredentialsPath ||
        process.env.GOOGLE_APPLICATION_CREDENTIALS
    )
  }

  private isConfigured(): boolean {
    return Boolean(env.googleSheetsSpreadsheetId && this.hasAuthSourceConfigured())
  }

  /**
   * Validates that GOOGLE_SHEETS_SPREADSHEET_ID is plausibly a real sheet ID and not
   * an OAuth Client ID that was accidentally pasted into the wrong env var.
   *
   * A real sheet ID is a ~44-char alphanumeric/dash/underscore string found in the
   * Google Sheets URL:  …/spreadsheets/d/<SHEET_ID>/edit
   */
  private getSpreadsheetId(): string {
    if (this.spreadsheetIdCache) return this.spreadsheetIdCache

    const raw = env.googleSheetsSpreadsheetId?.trim()
    if (!raw) throw new Error('GOOGLE_SHEETS_SPREADSHEET_ID is not set')

    // Reject OAuth Client IDs — including truncated variants ending in .co, .c, etc.
    if (OAUTH_CLIENT_ID_RE.test(raw)) {
      throw new Error(
        'GOOGLE_SHEETS_SPREADSHEET_ID looks like a Google OAuth Client ID, not a spreadsheet ID. ' +
          'Open your sheet in the browser and copy the ID from the URL: ' +
          'https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit'
      )
    }

    // Accept full sheet URLs — extract just the ID portion
    const urlMatch = raw.match(/\/spreadsheets\/d\/([a-zA-Z0-9-_]+)/)
    const normalized = urlMatch?.[1] ?? raw
    this.spreadsheetIdCache = normalized
    return normalized
  }

  private getA1Range(worksheetName: string, range: string): string {
    const escapedWorksheetName = worksheetName.replace(/'/g, "''")
    return `'${escapedWorksheetName}'!${range}`
  }

  private async getAuthClient() {
    const options: ConstructorParameters<typeof google.auth.GoogleAuth>[0] = {
      scopes: ['https://www.googleapis.com/auth/spreadsheets']
    }

    if (env.googleSheetsCredentialsJson) {
      options.credentials = JSON.parse(env.googleSheetsCredentialsJson)
    } else if (env.googleSheetsCredentialsPath) {
      const credPath = path.resolve(env.googleSheetsCredentialsPath)
      if (!fs.existsSync(credPath)) {
        throw new Error(
          `Google Sheets credentials file not found at: ${credPath}. ` +
            'Place your service account JSON at that path or set GOOGLE_SHEETS_CREDENTIALS_JSON.'
        )
      }
      options.keyFile = credPath
    }

    // If neither key file nor inline credentials are provided, GoogleAuth falls back to ADC.
    const auth = new google.auth.GoogleAuth(options)
    return auth.getClient()
  }

  private async withRetry<T>(action: () => Promise<T>, retries = 3, baseDelayMs = 250): Promise<T> {
    let lastError: Error | null = null

    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        return await action()
      } catch (err) {
        lastError = err as Error
        if (attempt === retries) break
        await new Promise((resolve) => setTimeout(resolve, baseDelayMs * attempt))
      }
    }

    throw lastError ?? new Error('Unknown Google Sheets retry failure')
  }

  private async resolveWorksheetName(sheets: SheetsClient): Promise<string> {
    if (env.googleSheetsWorksheetName) return env.googleSheetsWorksheetName
    if (this.worksheetNameCache) return this.worksheetNameCache

    const metadata = await sheets.spreadsheets.get({
      spreadsheetId: this.getSpreadsheetId(),
      includeGridData: false
    })

    const title = metadata.data.sheets?.[0]?.properties?.title
    if (!title) throw new Error('Unable to resolve worksheet name from spreadsheet metadata')

    this.worksheetNameCache = title
    return title
  }

  /**
   * Write the header row if cell A1 is empty.
   * Accepts an already-initialized sheets client so we do not create a second auth session.
   */
  private async ensureHeadersWithClient(sheets: SheetsClient, worksheetName: string): Promise<void> {
    const res = await this.withRetry(() =>
      sheets.spreadsheets.values.get({
        spreadsheetId: this.getSpreadsheetId(),
        range: this.getA1Range(worksheetName, 'A1:T1')
      })
    )

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
        'Education/Training Level',
        'Biggest Challenge',
        'Injury History',
        'Career Interests',
        'Top Recommendation',
        'Top Match %',
        'All Recommendations',
        'Motivation Recommendation'
      ]
      await this.withRetry(() =>
        sheets.spreadsheets.values.update({
          spreadsheetId: this.getSpreadsheetId(),
          range: this.getA1Range(worksheetName, 'A1'),
          valueInputOption: 'RAW',
          requestBody: { values: [headers] }
        })
      )
      logger.info('Google Sheets headers initialized')
    }
  }

  /**
   * Exports a questionnaire submission + its ML results to Google Sheets.
   * Failures are non-blocking and logged so they never break the submission response.
   */
  async exportSubmission(
    questionnaireResponse: IQuestionnaireResponse,
    recommendation: IPathwayRecommendation
  ): Promise<void> {
    if (!this.isConfigured()) {
      logger.warn('Google Sheets export skipped — missing sheet ID or credentials configuration')
      return
    }

    try {
      // Single auth round-trip shared by header check and row append
      const authClient = await this.getAuthClient()
      const sheets = google.sheets({ version: 'v4', auth: authClient as any })
      const worksheetName = await this.resolveWorksheetName(sheets)

      await this.ensureHeadersWithClient(sheets, worksheetName)

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
        questionnaireResponse.education_training_level,
        questionnaireResponse.biggest_challenge,
        questionnaireResponse.injury_history,
        questionnaireResponse.career_interests.join(', '),
        // ML predictions
        topRec?.pathwayName ?? '',
        topRec?.matchPercentage ?? '',
        recommendation.recommendations.map((r) => `${r.pathwayName}(${r.matchPercentage}%)`).join(' | '),
        recommendation.motivationRecommendation?.pathwayName ?? ''
      ]

      await this.withRetry(() =>
        sheets.spreadsheets.values.append({
          spreadsheetId: this.getSpreadsheetId(),
          range: this.getA1Range(worksheetName, 'A1:U1'),
          valueInputOption: 'RAW',
          requestBody: { values: [row] }
        })
      )

      logger.info('Questionnaire exported to Google Sheets successfully')
    } catch (err) {
      // Keep non-blocking — log at error level so it surfaces without failing the request
      logger.error('Google Sheets export failed', { error: (err as Error).message })
    }
  }

  /**
   * Call once at server startup to surface Google Sheets misconfiguration immediately
   * rather than discovering it silently at the first questionnaire submission.
   */
  validateConfig(): void {
    if (!env.googleSheetsSpreadsheetId) {
      logger.warn('Google Sheets disabled — GOOGLE_SHEETS_SPREADSHEET_ID not set')
      return
    }

    try {
      this.getSpreadsheetId() // validates the ID format
    } catch (err) {
      logger.error('Google Sheets misconfiguration detected at startup', {
        error: (err as Error).message
      })
      return
    }

    if (!this.hasAuthSourceConfigured()) {
      logger.warn(
        'Google Sheets disabled — no credentials configured. ' +
          'Set GOOGLE_SHEETS_CREDENTIALS_JSON, GOOGLE_SHEETS_CREDENTIALS_PATH, or GOOGLE_APPLICATION_CREDENTIALS.'
      )
      return
    }

    if (env.googleSheetsCredentialsPath) {
      const credPath = path.resolve(env.googleSheetsCredentialsPath)
      if (!fs.existsSync(credPath)) {
        logger.error('Google Sheets misconfiguration detected at startup', {
          error: `Credentials file not found: ${credPath}`
        })
        return
      }
    }

    logger.info('Google Sheets integration configured', {
      spreadsheetId: this.getSpreadsheetId(),
      credentialsSource: env.googleSheetsCredentialsJson
        ? 'inline JSON'
        : env.googleSheetsCredentialsPath
          ? `file: ${env.googleSheetsCredentialsPath}`
          : 'Application Default Credentials'
    })
  }
}

export const googleSheetsService = new GoogleSheetsService()
