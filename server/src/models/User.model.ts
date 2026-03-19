import mongoose, { Schema, type Document, type Model } from 'mongoose'
import bcrypt from 'bcryptjs'

export interface IUser extends Document {
  _id: mongoose.Types.ObjectId
  name: string
  email: string
  password: string
  role: 'athlete' | 'coach' | 'admin'
  createdAt: Date
  updatedAt: Date
  comparePassword(candidatePassword: string): Promise<boolean>
}

interface IUserModel extends Model<IUser> {}

const userSchema = new Schema<IUser>(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
      maxlength: [100, 'Name cannot exceed 100 characters']
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      lowercase: true,
      trim: true,
      match: [/^[^\s@]+@[^\s@]+\.[^\s@]+$/, 'Please provide a valid email']
    },
    password: {
      type: String,
      required: [true, 'Password is required'],
      minlength: [8, 'Password must be at least 8 characters'],
      select: false
    },
    role: {
      type: String,
      enum: ['athlete', 'coach', 'admin'],
      default: 'athlete'
    }
  },
  { timestamps: true }
)

userSchema.pre<IUser>('save', async function (next) {
  if (!this.isModified('password')) return next()
  this.password = await bcrypt.hash(this.password, 12)
  next()
})

userSchema.methods.comparePassword = function (
  this: IUser,
  candidatePassword: string
): Promise<boolean> {
  return bcrypt.compare(candidatePassword, this.password)
}

userSchema.methods.toJSON = function (this: IUser) {
  const obj = this.toObject() as Record<string, unknown>
  delete obj.password
  delete obj.__v
  return obj
}

const User = mongoose.model<IUser, IUserModel>('User', userSchema)
export default User
