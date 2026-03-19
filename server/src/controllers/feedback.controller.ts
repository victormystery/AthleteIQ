import type { Response, NextFunction } from 'express'
import type { AuthenticatedRequest } from '../types/index.js'
import { feedbackService } from '../services/feedback.service.js'
import { created, success } from '../utils/response.js'

export async function submitFeedback(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const feedback = await feedbackService.submit(req.user._id, req.body)
    created(res, { feedback }, 'Feedback submitted')
  } catch (err) {
    next(err)
  }
}

export async function getMyFeedback(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const feedbackList = await feedbackService.getMyFeedback(req.user._id)
    success(res, { feedback: feedbackList }, 'Feedback history retrieved')
  } catch (err) {
    next(err)
  }
}
