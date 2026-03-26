import type { Request, Response, NextFunction } from 'express'
import {
  User,
  PathwayRecommendation,
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
      .populate('questionnaireResponse')
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

export async function suspendUser(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const { id } = req.params
    const { suspended } = req.body

    if (typeof suspended !== 'boolean') {
      res.status(400).json({ success: false, message: 'suspended must be a boolean.' })
      return
    }

    const user = await User.findById(id)
    if (!user) {
      res.status(404).json({ success: false, message: 'User not found.' })
      return
    }
    if (user.role === 'admin') {
      res.status(403).json({ success: false, message: 'Admin accounts cannot be suspended.' })
      return
    }

    user.suspended = suspended
    await user.save()

    const updated = await User.findById(id).select('-password').lean()
    success(res, { user: updated }, suspended ? 'User suspended successfully' : 'User unsuspended successfully')
  } catch (err) {
    next(err)
  }
}

export async function updateUserRole(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const { id } = req.params
    const { role } = req.body

    const allowedRoles = ['student', 'career_advisor']
    if (!allowedRoles.includes(role)) {
      res.status(400).json({ success: false, message: 'Invalid role. Must be student or career_advisor.' })
      return
    }

    const user = await User.findById(id)
    if (!user) {
      res.status(404).json({ success: false, message: 'User not found.' })
      return
    }

    if (user.role === 'admin') {
      res.status(403).json({ success: false, message: 'Admin roles cannot be changed.' })
      return
    }

    user.role = role as 'student' | 'career_advisor'
    await user.save()

    const updated = await User.findById(id).select('-password').lean()
    success(res, { user: updated }, 'User role updated successfully')
  } catch (err) {
    next(err)
  }
}
