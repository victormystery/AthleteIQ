import { createRequire } from 'module'
import mongoose from 'mongoose'
import { UserProgress, type IUserProgress } from '../models/index.js'
import { careerService } from './career.service.js'
import { NotFoundError } from '../utils/errors.js'
import type { MilestoneStatus } from '../models/UserProgress.model.js'

// Load roadmap data at startup
const require = createRequire(import.meta.url)
// eslint-disable-next-line @typescript-eslint/no-require-imports
const roadmapData = require('../data/comprehensive_roadmaps.json') as {
  version: string
  pathways: Record<
    string,
    {
      title: string
      timeToEntry: string
      milestones: Array<{
        id: string
        title: string
        description: string
        type: string
        duration: string
        estimatedCost: string
        resources: Array<{ name: string; url: string }>
      }>
    }
  >
}

export interface RoadmapMilestone {
  id: string
  title: string
  description: string
  type: string
  duration: string
  estimatedCost: string
  resources: Array<{ name: string; url: string }>
  status: MilestoneStatus
  completedAt?: Date
  notes?: string
}

export interface RoadmapResult {
  pathwaySlug: string
  pathwayTitle: string
  timeToEntry: string
  milestones: RoadmapMilestone[]
  overallProgress: number
  startedAt?: Date
  lastActivityAt?: Date
}

export class RoadmapService {
  /**
   * Get personalised roadmap for a pathway, merged with user's progress.
   */
  async getRoadmap(userId: mongoose.Types.ObjectId, slug: string): Promise<RoadmapResult> {
    // Validate pathway exists
    const pathway = await careerService.getPathway(slug)
    const roadmapTemplate = roadmapData.pathways[slug]

    if (!roadmapTemplate) {
      throw new NotFoundError(`Roadmap for pathway "${slug}" not found`)
    }

    // Get user's progress record (if any)
    const progress = await UserProgress.findOne({ user: userId, pathwaySlug: slug })

    const milestones: RoadmapMilestone[] = roadmapTemplate.milestones.map((m) => {
      const saved = progress?.milestones.find((pm) => pm.milestoneId === m.id)
      return {
        ...m,
        status: saved?.status ?? 'not_started',
        completedAt: saved?.completedAt,
        notes: saved?.notes
      }
    })

    return {
      pathwaySlug: pathway.slug,
      pathwayTitle: pathway.title,
      timeToEntry: roadmapTemplate.timeToEntry,
      milestones,
      overallProgress: progress?.overallProgress ?? 0,
      startedAt: progress?.startedAt,
      lastActivityAt: progress?.lastActivityAt
    }
  }

  /**
   * Update a milestone's progress status.
   */
  async updateMilestoneProgress(
    userId: mongoose.Types.ObjectId,
    slug: string,
    milestoneId: string,
    milestoneTitle: string,
    status: MilestoneStatus,
    notes?: string
  ): Promise<IUserProgress> {
    // Validate roadmap exists
    const roadmapTemplate = roadmapData.pathways[slug]
    if (!roadmapTemplate) throw new NotFoundError(`Roadmap for "${slug}" not found`)

    const milestoneExists = roadmapTemplate.milestones.some((m) => m.id === milestoneId)
    if (!milestoneExists) throw new NotFoundError(`Milestone "${milestoneId}" not found`)

    // Upsert progress document
    let progress = await UserProgress.findOne({ user: userId, pathwaySlug: slug })

    if (!progress) {
      progress = await UserProgress.create({
        user: userId,
        pathwaySlug: slug,
        milestones: [],
        overallProgress: 0
      })
    }

    // Update or add milestone
    const existingIdx = progress.milestones.findIndex((m) => m.milestoneId === milestoneId)

    const milestoneUpdate = {
      milestoneId,
      title: milestoneTitle,
      status,
      notes,
      updatedAt: new Date(),
      ...(status === 'completed' ? { completedAt: new Date() } : {})
    }

    if (existingIdx >= 0) {
      progress.milestones[existingIdx] = {
        ...progress.milestones[existingIdx],
        ...milestoneUpdate
      }
    } else {
      progress.milestones.push(milestoneUpdate as any)
    }

    // Recalculate overall progress
    const totalMilestones = roadmapTemplate.milestones.length
    const completedCount = progress.milestones.filter((m) => m.status === 'completed').length
    progress.overallProgress = Math.round((completedCount / totalMilestones) * 100)
    progress.lastActivityAt = new Date()

    await progress.save()
    return progress
  }

  /**
   * Get a summary of all roadmaps the user has started.
   */
  async getSummary(userId: mongoose.Types.ObjectId): Promise<
    Array<{
      pathwaySlug: string
      pathwayTitle: string
      overallProgress: number
      lastActivityAt: Date
    }>
  > {
    const records = await UserProgress.find({ user: userId }).sort({ lastActivityAt: -1 }).lean()
    return records.map((r) => ({
      pathwaySlug: r.pathwaySlug,
      pathwayTitle: roadmapData.pathways[r.pathwaySlug]?.title ?? r.pathwaySlug,
      overallProgress: r.overallProgress,
      lastActivityAt: r.lastActivityAt
    }))
  }
}

export const roadmapService = new RoadmapService()
