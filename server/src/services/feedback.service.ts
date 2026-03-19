import mongoose from 'mongoose'
import {
  RecommendationFeedback,
  PathwayRecommendation,
  type IRecommendationFeedback
} from '../models/index.js'
import { NotFoundError } from '../utils/errors.js'

export interface FeedbackPayload {
  recommendationId: string
  pathwaySlug: string
  rating: number
  interested: boolean
  comment?: string
}

export class FeedbackService {
  /**
   * Submit feedback for a recommendation pathway.
   */
  async submit(
    userId: mongoose.Types.ObjectId,
    payload: FeedbackPayload
  ): Promise<IRecommendationFeedback> {
    // Verify the recommendation belongs to this user
    const recommendation = await PathwayRecommendation.findOne({
      _id: payload.recommendationId,
      user: userId
    })
    if (!recommendation) {
      throw new NotFoundError('Recommendation not found or does not belong to you')
    }

    // Upsert feedback (one per user per recommendation per pathway)
    const feedback = await RecommendationFeedback.findOneAndUpdate(
      {
        user: userId,
        recommendation: payload.recommendationId,
        pathwaySlug: payload.pathwaySlug
      },
      {
        rating: payload.rating,
        interested: payload.interested,
        comment: payload.comment
      },
      { new: true, upsert: true, runValidators: true }
    )

    return feedback!
  }

  /**
   * Get all feedback submitted by a user.
   */
  async getMyFeedback(userId: mongoose.Types.ObjectId): Promise<IRecommendationFeedback[]> {
    const docs = await RecommendationFeedback.find({ user: userId })
      .sort({ createdAt: -1 })
      .populate('recommendation', 'topRecommendation createdAt')
      .lean()
    return docs as unknown as IRecommendationFeedback[]
  }
}

export const feedbackService = new FeedbackService()
