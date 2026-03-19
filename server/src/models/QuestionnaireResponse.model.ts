import mongoose, { Schema, type Document, type Model } from 'mongoose'

export interface IQuestionnaireResponse extends Document {
  _id: mongoose.Types.ObjectId
  user: mongoose.Types.ObjectId
  // 14 input features
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
  // metadata
  submittedAt: Date
  createdAt: Date
  updatedAt: Date
}

interface IQuestionnaireResponseModel extends Model<IQuestionnaireResponse> {}

const questionnaireResponseSchema = new Schema<IQuestionnaireResponse>(
  {
    user: { type: Schema.Types.ObjectId, ref: 'User', required: true, index: true },
    academic_level: {
      type: String,
      required: true,
      enum: ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Postgraduate', 'Professional']
    },
    primary_sport: { type: String, required: true, trim: true },
    participation_years: {
      type: String,
      required: true,
      enum: ['< 1', '1-2', '3-5', '> 5']
    },
    participation_level: {
      type: String,
      required: true,
      enum: ['Not active', 'Recreational', 'Club', 'Regional', 'National', 'Elite']
    },
    fitness_level: { type: Number, required: true, min: 1, max: 5 },
    technical_skill: { type: Number, required: true, min: 1, max: 5 },
    leadership: { type: Number, required: true, min: 1, max: 5 },
    data_comfort: { type: Number, required: true, min: 1, max: 5 },
    motivation: {
      type: String,
      required: true,
      enum: ['Competition', 'Health', 'Coaching', 'Academic', 'Fame']
    },
    career_importance: {
      type: String,
      required: true,
      enum: [
        'Financial security',
        'Passion & purpose',
        'Work-life balance',
        'Career progression',
        'Social impact'
      ]
    },
    work_environment: {
      type: String,
      required: true,
      enum: ['Field', 'Office', 'Lab', 'Media', 'Mixed']
    },
    biggest_challenge: {
      type: String,
      required: true,
      enum: [
        'Lack of experience',
        'Academic pressure',
        'Financial constraints',
        'Injury & health',
        'Networking gaps',
        'Unclear goals'
      ]
    },
    injury_history: {
      type: String,
      required: true,
      enum: ['No injuries', 'Minor injuries', 'Significant injuries', 'Career-limiting injury']
    },
    career_interests: {
      type: [String],
      required: true,
      validate: {
        validator: (v: string[]) => v.length >= 1 && v.length <= 3,
        message: 'Select between 1 and 3 career interests'
      }
    },
    submittedAt: { type: Date, default: Date.now }
  },
  { timestamps: true }
)

// Index for history lookups
questionnaireResponseSchema.index({ user: 1, createdAt: -1 })

const QuestionnaireResponse = mongoose.model<
  IQuestionnaireResponse,
  IQuestionnaireResponseModel
>('QuestionnaireResponse', questionnaireResponseSchema)

export default QuestionnaireResponse
