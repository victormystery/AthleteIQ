import axios from 'axios'
import mongoose from 'mongoose'
import {
  CareerPathway,
  PathwayRecommendation,
  QuestionnaireResponse,
  type ICareerPathway,
  type IPathwayRecommendation,
  type IQuestionnaireResponse
} from '../models/index.js'
import { careerAnalysisService } from './careerAnalysis.service.js'
import { env } from '../config/env.js'
import { logger } from '../utils/logger.js'
import { NotFoundError, AppError } from '../utils/errors.js'

interface MLPredictPayload {
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

interface MLPredictResponse {
  predictions: Array<{ pathway: string; confidence: number }>
  model_version?: string
  processing_time_ms?: number
}

export class CareerService {
  /**
   * Submit questionnaire, call ML, persist recommendation.
   */
  async predict(
    userId: mongoose.Types.ObjectId,
    questionnaireResponseId: mongoose.Types.ObjectId,
    payload: MLPredictPayload
  ): Promise<IPathwayRecommendation> {
    const startTime = Date.now()

    // Fetch all active career pathways for enrichment
    const pathways = await CareerPathway.find({ isActive: true }).lean() as unknown as ICareerPathway[]
    if (pathways.length === 0) {
      throw new AppError('Career pathways not seeded. Run npm run seed first.', 503)
    }

    // Fetch the questionnaire response for analysis
    const qResponse = await QuestionnaireResponse.findById(questionnaireResponseId)
    if (!qResponse) throw new NotFoundError('Questionnaire response not found')

    // Call ML microservice (with graceful fallback)
    let mlResult: MLPredictResponse
    try {
      const mlPayload = this.toLegacyMlPayload(payload)
      const response = await axios.post<MLPredictResponse>(
        `${env.mlServiceUrl}/predict`,
        mlPayload,
        { timeout: 10000 }
      )
      mlResult = response.data
    } catch (err) {
      logger.warn('ML service unavailable — using rule-based fallback', {
        error: (err as Error).message
      })
      mlResult = this.ruleBasedFallback(payload, pathways)
    }

    // Build enriched recommendations
    const recommendations = mlResult.predictions
      .slice(0, 5)
      .map((pred, index) => {
        const slug = this.normaliseSlug(pred.pathway)
        const pathway = pathways.find((p) => p.slug === slug) ?? pathways[index]
        const insights = careerAnalysisService.getInsightsForPathway(
          { slug: pathway.slug, title: pathway.title, keySkills: pathway.keySkills },
          qResponse
        )

        return {
          pathwaySlug: pathway.slug,
          pathwayName: pathway.title,
          matchPercentage: Math.round(Math.min(pred.confidence, 0.60) * 100),
          confidence: pred.confidence,
          rank: index + 1,
          keySkillsMatch: pathway.keySkills.slice(0, 4),
          sportSpecificInsights: insights,
          salaryRange: pathway.salaryRange,
          jobGrowthOutlook: pathway.jobOutlook
        }
      })

    // Motivation-based recommendation
    const motivationRec = careerAnalysisService.getMotivationRecommendation(
      payload.motivation,
      pathways.map((p) => ({ slug: p.slug, title: p.title }))
    )

    const processingTimeMs = Date.now() - startTime

    const recommendation = await PathwayRecommendation.create({
      user: userId,
      questionnaireResponse: questionnaireResponseId,
      recommendations,
      motivationRecommendation: motivationRec,
      topRecommendation: recommendations[0]?.pathwaySlug ?? '',
      mlModelVersion: mlResult.model_version ?? '1.0.0',
      processingTimeMs
    })

    return recommendation
  }

  /**
   * Get user's most recent recommendations (populated).
   */
  async getRecommendations(userId: mongoose.Types.ObjectId): Promise<IPathwayRecommendation[]> {
    const docs = await PathwayRecommendation.find({ user: userId })
      .sort({ createdAt: -1 })
      .limit(10)
      .populate('questionnaireResponse')
      .lean()
    return docs as unknown as IPathwayRecommendation[]
  }

  /**
   * Get user's full assessment history.
   */
  async getHistory(userId: mongoose.Types.ObjectId): Promise<IPathwayRecommendation[]> {
    const docs = await PathwayRecommendation.find({ user: userId })
      .sort({ createdAt: -1 })
      .populate('questionnaireResponse')
      .lean()
    return docs as unknown as IPathwayRecommendation[]
  }

  /**
   * List all active career pathways.
   */
  async listPathways(): Promise<ICareerPathway[]> {
    const docs = await CareerPathway.find({ isActive: true }).sort({ title: 1 }).lean()
    return docs as unknown as ICareerPathway[]
  }

  /**
   * Get a single pathway by slug.
   */
  async getPathway(slug: string): Promise<ICareerPathway> {
    const pathway = await CareerPathway.findOne({ slug, isActive: true }).lean()
    if (!pathway) throw new NotFoundError(`Pathway "${slug}" not found`)
    return pathway as unknown as ICareerPathway
  }

  // ─── Private helpers ──────────────────────────────────────────────────────

  private normaliseSlug(pathwayName: string): string {
    return pathwayName
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^a-z0-9-]/g, '')
  }

  /**
   * Map current questionnaire labels to legacy values expected by the ML service.
   * This keeps ML inference stable while allowing richer UX labels in the product.
   */
  private toLegacyMlPayload(payload: MLPredictPayload): MLPredictPayload {
    const participationYearsMap: Record<string, string> = {
      'Less than 1 year': '< 1',
      '1-2 years': '1-2',
      '3-5 years': '3-5',
      'More than 5 years': '> 5'
    }

    const participationLevelMap: Record<string, string> = {
      'Not active': 'Not active',
      Recreational: 'Recreational',
      'University/School team': 'Club',
      'Club or academy': 'Regional',
      'Elite/competitive pathway': 'Elite'
    }

    const motivationMap: Record<string, string> = {
      'Competition and performance': 'Competition',
      'Health and fitness': 'Health',
      'Helping or coaching others': 'Coaching',
      'Academic or career opportunity': 'Academic',
      'Fame, media, or recognition': 'Fame'
    }

    const careerImportanceMap: Record<string, string> = {
      'Not important': 'Work-life balance',
      'Slightly important': 'Work-life balance',
      'Moderately important': 'Career progression',
      'Very important': 'Passion & purpose',
      'My main career focus': 'Passion & purpose'
    }

    const workEnvironmentMap: Record<string, string> = {
      'On-field / practical': 'Field',
      'Office / management': 'Office',
      'Laboratory / science / clinical': 'Lab',
      'Media / creative': 'Media',
      'A mix of environments': 'Mixed'
    }

    const biggestChallengeMap: Record<string, string> = {
      'Academic workload': 'Academic pressure',
      'Time management': 'Unclear goals',
      'Financial constraints': 'Financial constraints',
      'Injury risk or health': 'Injury & health',
      'Lack of facilities or coaching': 'Lack of experience',
      Motivation: 'Unclear goals'
    }

    const injuryHistoryMap: Record<string, string> = {
      None: 'No injuries',
      'Minor (short recovery)': 'Minor injuries',
      'Moderate (missed competitions)': 'Significant injuries',
      'Severe (long-term impact)': 'Career-limiting injury'
    }

    return {
      ...payload,
      participation_years: participationYearsMap[payload.participation_years] ?? payload.participation_years,
      participation_level: participationLevelMap[payload.participation_level] ?? payload.participation_level,
      motivation: motivationMap[payload.motivation] ?? payload.motivation,
      career_importance: careerImportanceMap[payload.career_importance] ?? payload.career_importance,
      work_environment: workEnvironmentMap[payload.work_environment] ?? payload.work_environment,
      biggest_challenge: biggestChallengeMap[payload.biggest_challenge] ?? payload.biggest_challenge,
      injury_history: injuryHistoryMap[payload.injury_history] ?? payload.injury_history
    }
  }

  /**
   * Rule-based fallback when ML microservice is unavailable.
   * Uses a simple scoring approach based on key questionnaire features.
   */
  private ruleBasedFallback(
    payload: MLPredictPayload,
    pathways: ICareerPathway[]
  ): MLPredictResponse {
    const scores: Record<string, number> = {}

    pathways.forEach((p) => {
      scores[p.slug] = 0.5 // Base score
    })

    // Leadership → coaching, teaching, management
    if (payload.leadership >= 4) scores['coaching-development'] = (scores['coaching-development'] ?? 0.5) + 0.15
    if (payload.leadership >= 4) scores['sports-management'] = (scores['sports-management'] ?? 0.5) + 0.10
    if (payload.leadership >= 4) scores['physical-education-teaching'] = (scores['physical-education-teaching'] ?? 0.5) + 0.08

    // Data comfort → analytics, science, law
    if (payload.data_comfort >= 4) scores['sports-analytics'] = (scores['sports-analytics'] ?? 0.5) + 0.15
    if (payload.data_comfort >= 3) scores['sports-science-medicine'] = (scores['sports-science-medicine'] ?? 0.5) + 0.10
    if (payload.data_comfort >= 3) scores['sports-law-ethics'] = (scores['sports-law-ethics'] ?? 0.5) + 0.05

    // High fitness → high performance, nutrition, fitness industry
    if (payload.fitness_level >= 4) scores['high-performance-sport'] = (scores['high-performance-sport'] ?? 0.5) + 0.15
    if (payload.fitness_level >= 3) scores['sports-nutrition'] = (scores['sports-nutrition'] ?? 0.5) + 0.10

    // Academic level → psychology, law, science
    if (payload.academic_level === 'Postgraduate') {
      scores['sports-psychology'] = (scores['sports-psychology'] ?? 0.5) + 0.10
      scores['sports-law-ethics'] = (scores['sports-law-ethics'] ?? 0.5) + 0.10
      scores['sports-science-medicine'] = (scores['sports-science-medicine'] ?? 0.5) + 0.05
    }

    // Motivation adjustments
    switch (payload.motivation) {
      case 'Helping or coaching others': scores['coaching-development'] = (scores['coaching-development'] ?? 0.5) + 0.20; scores['physical-education-teaching'] = (scores['physical-education-teaching'] ?? 0.5) + 0.10; break
      case 'Health and fitness': scores['sports-science-medicine'] = (scores['sports-science-medicine'] ?? 0.5) + 0.15; scores['recreational-fitness-industry'] = (scores['recreational-fitness-industry'] ?? 0.5) + 0.10; scores['sports-nutrition'] = (scores['sports-nutrition'] ?? 0.5) + 0.10; break
      case 'Competition and performance': scores['high-performance-sport'] = (scores['high-performance-sport'] ?? 0.5) + 0.20; scores['sports-psychology'] = (scores['sports-psychology'] ?? 0.5) + 0.05; break
      case 'Academic or career opportunity': scores['sports-science-medicine'] = (scores['sports-science-medicine'] ?? 0.5) + 0.20; scores['sports-psychology'] = (scores['sports-psychology'] ?? 0.5) + 0.10; scores['physical-education-teaching'] = (scores['physical-education-teaching'] ?? 0.5) + 0.05; break
      case 'Fame, media, or recognition': scores['sports-media-journalism'] = (scores['sports-media-journalism'] ?? 0.5) + 0.20; scores['sports-law-ethics'] = (scores['sports-law-ethics'] ?? 0.5) + 0.05; break
    }

    // Work environment
    switch (payload.work_environment) {
      case 'On-field / practical': scores['coaching-development'] = (scores['coaching-development'] ?? 0.5) + 0.05; scores['high-performance-sport'] = (scores['high-performance-sport'] ?? 0.5) + 0.05; scores['physical-education-teaching'] = (scores['physical-education-teaching'] ?? 0.5) + 0.08; break
      case 'Laboratory / science / clinical': scores['sports-science-medicine'] = (scores['sports-science-medicine'] ?? 0.5) + 0.10; scores['sports-analytics'] = (scores['sports-analytics'] ?? 0.5) + 0.05; scores['sports-nutrition'] = (scores['sports-nutrition'] ?? 0.5) + 0.05; break
      case 'Office / management': scores['sports-management'] = (scores['sports-management'] ?? 0.5) + 0.10; scores['sports-law-ethics'] = (scores['sports-law-ethics'] ?? 0.5) + 0.10; scores['sports-psychology'] = (scores['sports-psychology'] ?? 0.5) + 0.05; break
      case 'Media / creative': scores['sports-media-journalism'] = (scores['sports-media-journalism'] ?? 0.5) + 0.15; break
      case 'A mix of environments': scores['sports-psychology'] = (scores['sports-psychology'] ?? 0.5) + 0.05; scores['sports-nutrition'] = (scores['sports-nutrition'] ?? 0.5) + 0.05; break
    }

    // Sort and scale to a realistic confidence range (0.48–0.85)
    // so no pathway ever shows 100% and scores feel genuinely differentiated.
    const sorted = Object.entries(scores)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 5)

    const maxScore = sorted[0][1]
    const minScore = sorted[sorted.length - 1][1]
    const scoreRange = maxScore - minScore || 0.01

    const predictions = sorted.map(([slug, score]) => ({
      pathway: slug,
      confidence: 0.40 + ((score - minScore) / scoreRange) * 0.20
    }))

    return { predictions, model_version: 'fallback-1.0.0' }
  }
}

export const careerService = new CareerService()
