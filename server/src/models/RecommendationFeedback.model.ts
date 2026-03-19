import mongoose, { Schema, type Document, type Model } from 'mongoose'

export interface IRecommendationFeedback extends Document {
  _id: mongoose.Types.ObjectId
  user: mongoose.Types.ObjectId
  recommendation: mongoose.Types.ObjectId
  pathwaySlug: string
  rating: number
  interested: boolean
  comment?: string
  createdAt: Date
  updatedAt: Date
}

interface IRecommendationFeedbackModel extends Model<IRecommendationFeedback> {}

const recommendationFeedbackSchema = new Schema<IRecommendationFeedback>(
  {
    user: { type: Schema.Types.ObjectId, ref: 'User', required: true, index: true },
    recommendation: {
      type: Schema.Types.ObjectId,
      ref: 'PathwayRecommendation',
      required: true
    },
    pathwaySlug: { type: String, required: true, trim: true },
    rating: { type: Number, required: true, min: 1, max: 5 },
    interested: { type: Boolean, required: true },
    comment: { type: String, trim: true, maxlength: [1000, 'Comment cannot exceed 1000 characters'] }
  },
  { timestamps: true }
)

recommendationFeedbackSchema.index({ user: 1, createdAt: -1 })
recommendationFeedbackSchema.index({ recommendation: 1, pathwaySlug: 1 })

const RecommendationFeedback = mongoose.model<
  IRecommendationFeedback,
  IRecommendationFeedbackModel
>('RecommendationFeedback', recommendationFeedbackSchema)

export default RecommendationFeedback
