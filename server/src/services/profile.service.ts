import mongoose from 'mongoose'
import { Profile, type IProfile } from '../models/index.js'
import { NotFoundError } from '../utils/errors.js'

export interface ProfileUpdatePayload {
  university?: string
  programOfStudy?: string
  primarySport?: string
  yearOfStudy?: string
  avatarUrl?: string
  bio?: string
}

export class ProfileService {
  /**
   * Get profile for a user. Creates one if it doesn't exist.
   */
  async getOrCreateProfile(userId: mongoose.Types.ObjectId): Promise<IProfile> {
    let profile = await Profile.findOne({ user: userId })
    if (!profile) {
      profile = await Profile.create({ user: userId })
    }
    return profile
  }

  /**
   * Update profile fields for a user.
   */
  async updateProfile(
    userId: mongoose.Types.ObjectId,
    payload: ProfileUpdatePayload
  ): Promise<IProfile> {
    const allowedFields: (keyof ProfileUpdatePayload)[] = [
      'university',
      'programOfStudy',
      'primarySport',
      'yearOfStudy',
      'avatarUrl',
      'bio'
    ]

    const updates: Partial<ProfileUpdatePayload> = {}
    for (const field of allowedFields) {
      if (payload[field] !== undefined) {
        updates[field] = payload[field]
      }
    }

    const profile = await Profile.findOneAndUpdate(
      { user: userId },
      { $set: updates },
      { new: true, upsert: true, runValidators: true }
    )

    if (!profile) throw new NotFoundError('Profile not found')
    return profile
  }
}

export const profileService = new ProfileService()
