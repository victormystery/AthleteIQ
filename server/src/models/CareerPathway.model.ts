import mongoose, { Schema, type Document, type Model } from 'mongoose'

export interface ICareerProgressionStep {
  level: string
  title: string
  yearsExperience: string
  description: string
}

export interface ISuccessStory {
  name: string
  sport: string
  career: string
  quote: string
}

export interface ICareerPathway extends Document {
  _id: mongoose.Types.ObjectId
  title: string
  slug: string
  icon: string
  colour: string
  category: string
  description: string
  workEnvironment: string[]
  jobOutlook: string
  salaryRange: { min: number; max: number; currency: string }
  educationRequirements: string[]
  keySkills: string[]
  certifications: string[]
  careerProgressionSteps: ICareerProgressionStep[]
  successStories: ISuccessStory[]
  isActive: boolean
  createdAt: Date
  updatedAt: Date
}

interface ICareerPathwayModel extends Model<ICareerPathway> {}

const careerPathwaySchema = new Schema<ICareerPathway>(
  {
    title: { type: String, required: true, trim: true },
    slug: { type: String, required: true, unique: true, lowercase: true, trim: true, index: true },
    icon: { type: String, default: '🏃' },
    colour: { type: String, default: '#3B82F6' },
    category: { type: String, required: true, trim: true },
    description: { type: String, required: true },
    workEnvironment: [{ type: String }],
    jobOutlook: { type: String, default: 'Stable' },
    salaryRange: {
      min: { type: Number, default: 0 },
      max: { type: Number, default: 0 },
      currency: { type: String, default: 'USD' }
    },
    educationRequirements: [{ type: String }],
    keySkills: [{ type: String }],
    certifications: [{ type: String }],
    careerProgressionSteps: [
      {
        level: String,
        title: String,
        yearsExperience: String,
        description: String
      }
    ],
    successStories: [
      {
        name: String,
        sport: String,
        career: String,
        quote: String
      }
    ],
    isActive: { type: Boolean, default: true }
  },
  { timestamps: true }
)

const CareerPathway = mongoose.model<ICareerPathway, ICareerPathwayModel>(
  'CareerPathway',
  careerPathwaySchema
)
export default CareerPathway
