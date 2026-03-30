import mongoose, { Schema, type Document, type Model } from 'mongoose'

export interface IQuestionnaireResponse extends Document {
  _id: mongoose.Types.ObjectId
  user: mongoose.Types.ObjectId
  // questionnaire input features
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
  education_training_level: string
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
      enum: ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Postgraduate']
    },
    primary_sport: { type: String, required: true, trim: true },
    participation_years: {
      type: String,
      required: true,
      enum: ['Less than 1 year', '1-2 years', '3-5 years', 'More than 5 years']
    },
    participation_level: {
      type: String,
      required: true,
      enum: ['Not active', 'Recreational', 'University/School team', 'Club or academy', 'Elite/competitive pathway']
    },
    fitness_level: { type: Number, required: true, min: 1, max: 5 },
    technical_skill: { type: Number, required: true, min: 1, max: 5 },
    leadership: { type: Number, required: true, min: 1, max: 5 },
    data_comfort: { type: Number, required: true, min: 1, max: 5 },
    motivation: {
      type: String,
      required: true,
      enum: ['Competition and performance', 'Health and fitness', 'Helping or coaching others', 'Academic or career opportunity', 'Fame, media, or recognition']
    },
    career_importance: {
      type: String,
      required: true,
      enum: [
        'Not important',
        'Slightly important',
        'Moderately important',
        'Very important',
        'My main career focus'
      ]
    },
    work_environment: {
      type: String,
      required: true,
      enum: ['On-field / practical', 'Office / management', 'Laboratory / science / clinical', 'Media / creative', 'A mix of environments']
    },
    education_training_level: {
      type: String,
      required: true,
      enum: [
        'Short courses or certifications only',
        'Diploma',
        "Bachelor's degree or add-on program",
        "Master's degree",
        'Medical/clinical or doctoral pathway'
      ]
    },
    biggest_challenge: {
      type: String,
      required: true,
      enum: [
        'Academic workload',
        'Time management',
        'Financial constraints',
        'Injury risk or health',
        'Lack of facilities or coaching',
        'Motivation'
      ]
    },
    injury_history: {
      type: String,
      required: true,
      enum: ['None', 'Minor (short recovery)', 'Moderate (missed competitions)', 'Severe (long-term impact)']
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
