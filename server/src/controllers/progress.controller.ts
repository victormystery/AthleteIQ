import type { Response, NextFunction } from 'express'
import type { AuthenticatedRequest } from '../types/index.js'
import { progressService } from '../services/progress.service.js'
import { success } from '../utils/response.js'

export async function upsertProgress(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const progress = await progressService.upsertProgress(req.user._id, req.body)
    success(res, { progress }, 'Progress updated')
  } catch (err) {
    next(err)
  }
}

export async function getMyProgress(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const progress = await progressService.getMyProgress(req.user._id)
    success(res, { progress }, 'Progress records retrieved')
  } catch (err) {
    next(err)
  }
}
