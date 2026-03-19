import type { Request, Response, NextFunction } from 'express'
import {
  User,
  PathwayRecommendation,
  QuestionnaireResponse,
  RecommendationFeedback
} from '../models/index.js'
import { success } from '../utils/response.js'

export async function getDashboardStats(
  _req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const [
      totalUsers,
      totalStudents,
      totalAdvisors,
      totalAssessments,
      totalFeedback,
      recentUsers
    ] = await Promise.all([
      User.countDocuments(),
      User.countDocuments({ role: 'student' }),
      User.countDocuments({ role: 'career_advisor' }),
      PathwayRecommendation.countDocuments(),
      RecommendationFeedback.countDocuments(),
      User.find().sort({ createdAt: -1 }).limit(10).select('-password').lean()
    ])

    success(
      res,
      {
        stats: {
          totalUsers,
          totalStudents,
          totalAdvisors,
          totalAssessments,
          totalFeedback
        },
        recentUsers
      },
      'Admin dashboard data retrieved'
    )
  } catch (err) {
    next(err)
  }
}

export async function listUsers(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const page = Math.max(1, parseInt(req.query.page as string) || 1)
    const limit = Math.min(100, parseInt(req.query.limit as string) || 20)
    const skip = (page - 1) * limit

    const [users, total] = await Promise.all([
      User.find().sort({ createdAt: -1 }).skip(skip).limit(limit).select('-password').lean(),
      User.countDocuments()
    ])

    success(
      res,
      {
        users,
        pagination: { page, limit, total, pages: Math.ceil(total / limit) }
      },
      'Users retrieved'
    )
  } catch (err) {
    next(err)
  }
}

export async function getRecentAssessments(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const limit = Math.min(50, parseInt(req.query.limit as string) || 20)
    const assessments = await PathwayRecommendation.find()
      .sort({ createdAt: -1 })
      .limit(limit)
      .populate('user', 'name email role')
      .populate('questionnaireResponse', 'primary_sport academic_level')
      .lean()

    success(res, { assessments }, 'Recent assessments retrieved')
  } catch (err) {
    next(err)
  }
}

export async function deleteUser(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const { id } = req.params
    await User.findByIdAndDelete(id)
    success(res, null, 'User deleted successfully')
  } catch (err) {
    next(err)
  }
}
