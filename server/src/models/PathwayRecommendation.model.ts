import mongoose, { Schema, type Document, type Model } from 'mongoose'

export interface IRecommendedPathway {
  pathwaySlug: string
  pathwayName: string
  matchPercentage: number
  confidence: number
  rank: number
  keySkillsMatch: string[]
  sportSpecificInsights: string[]
  salaryRange: { min: number; max: number; currency: string }
  jobGrowthOutlook: string
}

export interface IMotivationRecommendation {
  pathwaySlug: string
  pathwayName: string
  reason: string
}

export interface IPathwayRecommendation extends Document {
  _id: mongoose.Types.ObjectId
  user: mongoose.Types.ObjectId
  questionnaireResponse: mongoose.Types.ObjectId
  recommendations: IRecommendedPathway[]
  motivationRecommendation: IMotivationRecommendation
  topRecommendation: string
  mlModelVersion: string
  processingTimeMs: number
  createdAt: Date
  updatedAt: Date
}

interface IPathwayRecommendationModel extends Model<IPathwayRecommendation> {}

const pathwayRecommendationSchema = new Schema<IPathwayRecommendation>(
  {
    user: { type: Schema.Types.ObjectId, ref: 'User', required: true, index: true },
    questionnaireResponse: {
      type: Schema.Types.ObjectId,
      ref: 'QuestionnaireResponse',
      required: true
    },
    recommendations: [
      {
        pathwaySlug: { type: String, required: true },
        pathwayName: { type: String, required: true },
        matchPercentage: { type: Number, required: true, min: 0, max: 100 },
        confidence: { type: Number, required: true, min: 0, max: 1 },
        rank: { type: Number, required: true },
        keySkillsMatch: [String],
        sportSpecificInsights: [String],
        salaryRange: {
          min: { type: Number, default: 0 },
          max: { type: Number, default: 0 },
          currency: { type: String, default: 'USD' }
        },
        jobGrowthOutlook: { type: String, default: 'Stable' }
      }
    ],
    motivationRecommendation: {
      pathwaySlug: { type: String },
      pathwayName: { type: String },
      reason: { type: String }
    },
    topRecommendation: { type: String },
    mlModelVersion: { type: String, default: '1.0.0' },
    processingTimeMs: { type: Number, default: 0 }
  },
  { timestamps: true }
)

pathwayRecommendationSchema.index({ user: 1, createdAt: -1 })

const PathwayRecommendation = mongoose.model<
  IPathwayRecommendation,
  IPathwayRecommendationModel
>('PathwayRecommendation', pathwayRecommendationSchema)

export default PathwayRecommendation
