import { User } from '../models/index.js'
import type { IUser } from '../models/User.model.js'
import { NotFoundError } from '../utils/errors.js'
import type mongoose from 'mongoose'

export async function getProfile(userId: string | mongoose.Types.ObjectId): Promise<IUser> {
  const user = await User.findById(userId)
  if (!user) throw new NotFoundError('User not found')
  return user
}

export async function updateProfile(
  userId: string | mongoose.Types.ObjectId,
  updates: Partial<Pick<IUser, 'name'>>
): Promise<IUser> {
  const allowed: Array<keyof IUser> = ['name']
  const filtered = Object.fromEntries(
    Object.entries(updates).filter(([k]) => allowed.includes(k as keyof IUser))
  )
  const user = await User.findByIdAndUpdate(userId, filtered, { new: true, runValidators: true })
  if (!user) throw new NotFoundError('User not found')
  return user
}
