import mongoose from 'mongoose'
import { UserProgress, type IUserProgress } from '../models/index.js'
import type { MilestoneStatus } from '../models/UserProgress.model.js'
import { NotFoundError } from '../utils/errors.js'

export interface ProgressPayload {
  pathwaySlug: string
  milestoneId: string
  milestoneTitle: string
  status: MilestoneStatus
  notes?: string
}

export class ProgressService {
  /**
   * Create or update a milestone progress record.
   */
  async upsertProgress(
    userId: mongoose.Types.ObjectId,
    payload: ProgressPayload
  ): Promise<IUserProgress> {
    let progress = await UserProgress.findOne({
      user: userId,
      pathwaySlug: payload.pathwaySlug
    })

    if (!progress) {
      progress = await UserProgress.create({
        user: userId,
        pathwaySlug: payload.pathwaySlug,
        milestones: [],
        overallProgress: 0
      })
    }

    const existingIdx = progress.milestones.findIndex(
      (m) => m.milestoneId === payload.milestoneId
    )

    const milestoneUpdate = {
      milestoneId: payload.milestoneId,
      title: payload.milestoneTitle,
      status: payload.status,
      notes: payload.notes,
      updatedAt: new Date(),
      ...(payload.status === 'completed' ? { completedAt: new Date() } : {})
    }

    if (existingIdx >= 0) {
      progress.milestones[existingIdx] = {
        ...progress.milestones[existingIdx],
        ...milestoneUpdate
      }
    } else {
      progress.milestones.push(milestoneUpdate as any)
    }

    const completedCount = progress.milestones.filter((m) => m.status === 'completed').length
    progress.overallProgress =
      progress.milestones.length > 0
        ? Math.round((completedCount / progress.milestones.length) * 100)
        : 0
    progress.lastActivityAt = new Date()

    await progress.save()
    return progress
  }

  /**
   * Get all progress records for a user.
   */
  async getMyProgress(userId: mongoose.Types.ObjectId): Promise<IUserProgress[]> {
    const docs = await UserProgress.find({ user: userId }).sort({ lastActivityAt: -1 }).lean()
    return docs as unknown as IUserProgress[]
  }

  /**
   * Get progress for a specific pathway.
   */
  async getPathwayProgress(
    userId: mongoose.Types.ObjectId,
    slug: string
  ): Promise<IUserProgress | null> {
    const doc = await UserProgress.findOne({ user: userId, pathwaySlug: slug }).lean()
    return doc as unknown as IUserProgress | null
  }
}

export const progressService = new ProgressService()
