import mongoose, { Schema, type Document, type Model } from 'mongoose'

export type MilestoneStatus = 'not_started' | 'in_progress' | 'completed'

export interface IMilestoneProgress {
  milestoneId: string
  title: string
  status: MilestoneStatus
  completedAt?: Date
  notes?: string
  updatedAt: Date
}

export interface IUserProgress extends Document {
  _id: mongoose.Types.ObjectId
  user: mongoose.Types.ObjectId
  pathwaySlug: string
  milestones: IMilestoneProgress[]
  overallProgress: number // 0–100 percentage
  startedAt: Date
  lastActivityAt: Date
  createdAt: Date
  updatedAt: Date
}

interface IUserProgressModel extends Model<IUserProgress> {}

const milestoneProgressSchema = new Schema<IMilestoneProgress>(
  {
    milestoneId: { type: String, required: true },
    title: { type: String, required: true },
    status: {
      type: String,
      enum: ['not_started', 'in_progress', 'completed'],
      default: 'not_started'
    },
    completedAt: { type: Date },
    notes: { type: String, trim: true, maxlength: [1000, 'Notes cannot exceed 1000 characters'] },
    updatedAt: { type: Date, default: Date.now }
  },
  { _id: false }
)

const userProgressSchema = new Schema<IUserProgress>(
  {
    user: { type: Schema.Types.ObjectId, ref: 'User', required: true, index: true },
    pathwaySlug: { type: String, required: true, trim: true },
    milestones: [milestoneProgressSchema],
    overallProgress: { type: Number, default: 0, min: 0, max: 100 },
    startedAt: { type: Date, default: Date.now },
    lastActivityAt: { type: Date, default: Date.now }
  },
  { timestamps: true }
)

// One progress record per user per pathway
userProgressSchema.index({ user: 1, pathwaySlug: 1 }, { unique: true })

const UserProgress = mongoose.model<IUserProgress, IUserProgressModel>(
  'UserProgress',
  userProgressSchema
)
export default UserProgress
