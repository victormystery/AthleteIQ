import type { Response, NextFunction } from 'express'
import type { AuthenticatedRequest } from '../types/index.js'
import { roadmapService } from '../services/roadmap.service.js'
import { success } from '../utils/response.js'

export async function getPathwayRoadmap(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const roadmap = await roadmapService.getRoadmap(req.user._id, req.params.slug)
    success(res, { roadmap }, 'Roadmap retrieved')
  } catch (err) {
    next(err)
  }
}

export async function getRoadmapSummary(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const summary = await roadmapService.getSummary(req.user._id)
    success(res, { summary }, 'Roadmap summary retrieved')
  } catch (err) {
    next(err)
  }
}

export async function updateRoadmapProgress(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const { slug } = req.params
    const { milestoneId, milestoneTitle, status, notes } = req.body

    const progress = await roadmapService.updateMilestoneProgress(
      req.user._id,
      slug,
      milestoneId,
      milestoneTitle,
      status,
      notes
    )
    success(res, { progress }, 'Milestone progress updated')
  } catch (err) {
    next(err)
  }
}
