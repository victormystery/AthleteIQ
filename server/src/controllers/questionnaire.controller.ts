import type { Response, NextFunction } from 'express'
import type { AuthenticatedRequest } from '../types/index.js'
import { questionnaireService } from '../services/questionnaire.service.js'
import { created, success } from '../utils/response.js'

export async function submitQuestionnaire(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const result = await questionnaireService.submit(req.user._id, req.body)
    created(res, result, 'Questionnaire submitted and recommendations generated')
  } catch (err) {
    next(err)
  }
}

export async function getMyQuestionnaires(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const responses = await questionnaireService.getHistory(req.user._id)
    success(res, { responses }, 'Questionnaire history retrieved')
  } catch (err) {
    next(err)
  }
}
