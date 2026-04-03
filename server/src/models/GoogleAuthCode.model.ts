import mongoose, { Schema, type Document, type Model } from 'mongoose'

export interface IGoogleAuthCode extends Document {
  code: string
  userId: mongoose.Types.ObjectId
  expiresAt: Date
  usedAt?: Date
  createdAt: Date
  updatedAt: Date
}

interface IGoogleAuthCodeModel extends Model<IGoogleAuthCode> {}

const googleAuthCodeSchema = new Schema<IGoogleAuthCode>(
  {
    code: {
      type: String,
      required: true,
      unique: true,
      index: true
    },
    userId: {
      type: Schema.Types.ObjectId,
      ref: 'User',
      required: true,
      index: true
    },
    expiresAt: {
      type: Date,
      required: true,
      index: true
    },
    usedAt: {
      type: Date,
      default: undefined,
      index: true
    }
  },
  { timestamps: true }
)

googleAuthCodeSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 })

const GoogleAuthCode = mongoose.model<IGoogleAuthCode, IGoogleAuthCodeModel>(
  'GoogleAuthCode',
  googleAuthCodeSchema
)

export default GoogleAuthCode
