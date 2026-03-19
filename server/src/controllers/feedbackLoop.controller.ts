import type { Request, Response, NextFunction } from 'express'
import { feedbackLoopService } from '../services/feedbackLoop.service.js'
import { success } from '../utils/response.js'

export async function getInsights(
  _req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const insights = await feedbackLoopService.getInsights()
    success(res, { insights }, 'Feedback loop insights retrieved')
  } catch (err) {
    next(err)
  }
}

export async function getPathwayBreakdown(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const breakdown = await feedbackLoopService.getPathwayBreakdown(req.params.slug)
    if (!breakdown) {
      success(res, { breakdown: null }, 'No feedback found for this pathway')
      return
    }
    success(res, { breakdown }, 'Pathway feedback breakdown retrieved')
  } catch (err) {
    next(err)
  }
}
