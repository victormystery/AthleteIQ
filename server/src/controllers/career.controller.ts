import type { Request, Response, NextFunction } from 'express'
import type { AuthenticatedRequest } from '../types/index.js'
import { careerService } from '../services/career.service.js'
import { success } from '../utils/response.js'

export async function listPathways(
  _req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const pathways = await careerService.listPathways()
    success(res, { pathways }, 'Career pathways retrieved')
  } catch (err) {
    next(err)
  }
}

export async function getPathway(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const pathway = await careerService.getPathway(req.params.slug)
    success(res, { pathway }, 'Pathway retrieved')
  } catch (err) {
    next(err)
  }
}

export async function getRecommendations(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const recommendations = await careerService.getRecommendations(req.user._id)
    success(res, { recommendations }, 'Recommendations retrieved')
  } catch (err) {
    next(err)
  }
}

export async function getHistory(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const history = await careerService.getHistory(req.user._id)
    success(res, { history }, 'Assessment history retrieved')
  } catch (err) {
    next(err)
  }
}
