import mongoose, { Schema, type Document, type Model } from 'mongoose'

export interface IProfile extends Document {
  _id: mongoose.Types.ObjectId
  user: mongoose.Types.ObjectId
  university: string
  programOfStudy: string
  primarySport: string
  yearOfStudy: string
  avatarUrl?: string
  bio?: string
  createdAt: Date
  updatedAt: Date
}

interface IProfileModel extends Model<IProfile> {}

const profileSchema = new Schema<IProfile>(
  {
    user: {
      type: Schema.Types.ObjectId,
      ref: 'User',
      required: true,
      unique: true,
      index: true
    },
    university: {
      type: String,
      trim: true,
      maxlength: [200, 'University name cannot exceed 200 characters'],
      default: ''
    },
    programOfStudy: {
      type: String,
      trim: true,
      maxlength: [200, 'Program cannot exceed 200 characters'],
      default: ''
    },
    primarySport: {
      type: String,
      trim: true,
      maxlength: [100, 'Sport cannot exceed 100 characters'],
      default: ''
    },
    yearOfStudy: {
      type: String,
      enum: ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Postgraduate', 'Professional', ''],
      default: ''
    },
    avatarUrl: {
      type: String,
      trim: true
    },
    bio: {
      type: String,
      trim: true,
      maxlength: [500, 'Bio cannot exceed 500 characters']
    }
  },
  { timestamps: true }
)

const Profile = mongoose.model<IProfile, IProfileModel>('Profile', profileSchema)
export default Profile
