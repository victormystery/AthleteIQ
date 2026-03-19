import type { Response, NextFunction } from 'express'
import type { AuthenticatedRequest } from '../types/index.js'
import { profileService } from '../services/profile.service.js'
import { success } from '../utils/response.js'

export async function getMyProfile(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const profile = await profileService.getOrCreateProfile(req.user._id)
    success(res, { profile }, 'Profile retrieved')
  } catch (err) {
    next(err)
  }
}

export async function updateMyProfile(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const profile = await profileService.updateProfile(req.user._id, req.body)
    success(res, { profile }, 'Profile updated')
  } catch (err) {
    next(err)
  }
}
