import { RecommendationFeedback, PathwayRecommendation } from '../models/index.js'

export interface PathwayFeedbackSummary {
  pathwaySlug: string
  totalFeedback: number
  averageRating: number
  interestedCount: number
  notInterestedCount: number
  interestedRate: number
}

export interface FeedbackLoopInsights {
  totalSubmissions: number
  totalFeedback: number
  pathwaySummaries: PathwayFeedbackSummary[]
  topRatedPathway: string
  mostInterestingPathway: string
  averageRatingOverall: number
  generatedAt: Date
}

export class FeedbackLoopService {
  /**
   * Aggregate feedback across all users for model improvement signals.
   */
  async getInsights(): Promise<FeedbackLoopInsights> {
    const [totalSubmissions, totalFeedback] = await Promise.all([
      PathwayRecommendation.countDocuments(),
      RecommendationFeedback.countDocuments()
    ])

    const aggregation = await RecommendationFeedback.aggregate([
      {
        $group: {
          _id: '$pathwaySlug',
          totalFeedback: { $sum: 1 },
          averageRating: { $avg: '$rating' },
          interestedCount: {
            $sum: { $cond: ['$interested', 1, 0] }
          },
          notInterestedCount: {
            $sum: { $cond: ['$interested', 0, 1] }
          }
        }
      },
      { $sort: { averageRating: -1 } }
    ])

    const pathwaySummaries: PathwayFeedbackSummary[] = aggregation.map((a) => ({
      pathwaySlug: a._id,
      totalFeedback: a.totalFeedback,
      averageRating: Math.round(a.averageRating * 100) / 100,
      interestedCount: a.interestedCount,
      notInterestedCount: a.notInterestedCount,
      interestedRate:
        a.totalFeedback > 0 ? Math.round((a.interestedCount / a.totalFeedback) * 100) : 0
    }))

    const overallAvg =
      pathwaySummaries.length > 0
        ? pathwaySummaries.reduce((sum, p) => sum + p.averageRating, 0) / pathwaySummaries.length
        : 0

    const topRated = [...pathwaySummaries].sort((a, b) => b.averageRating - a.averageRating)[0]
    const mostInteresting = [...pathwaySummaries].sort(
      (a, b) => b.interestedRate - a.interestedRate
    )[0]

    return {
      totalSubmissions,
      totalFeedback,
      pathwaySummaries,
      topRatedPathway: topRated?.pathwaySlug ?? 'N/A',
      mostInterestingPathway: mostInteresting?.pathwaySlug ?? 'N/A',
      averageRatingOverall: Math.round(overallAvg * 100) / 100,
      generatedAt: new Date()
    }
  }

  /**
   * Get per-pathway aggregated feedback (for admin view).
   */
  async getPathwayBreakdown(slug: string): Promise<PathwayFeedbackSummary | null> {
    const result = await RecommendationFeedback.aggregate([
      { $match: { pathwaySlug: slug } },
      {
        $group: {
          _id: '$pathwaySlug',
          totalFeedback: { $sum: 1 },
          averageRating: { $avg: '$rating' },
          interestedCount: { $sum: { $cond: ['$interested', 1, 0] } },
          notInterestedCount: { $sum: { $cond: ['$interested', 0, 1] } }
        }
      }
    ])

    if (result.length === 0) return null

    const a = result[0]
    return {
      pathwaySlug: a._id,
      totalFeedback: a.totalFeedback,
      averageRating: Math.round(a.averageRating * 100) / 100,
      interestedCount: a.interestedCount,
      notInterestedCount: a.notInterestedCount,
      interestedRate:
        a.totalFeedback > 0 ? Math.round((a.interestedCount / a.totalFeedback) * 100) : 0
    }
  }
}

export const feedbackLoopService = new FeedbackLoopService()
