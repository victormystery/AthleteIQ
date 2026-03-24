import { Router } from 'express'
import { authenticate } from '../middleware/auth.middleware.js'
import { validate } from '../middleware/validate.middleware.js'
import { roadmapProgressSchema } from '../validators/progress.validator.js'
import {
  getPathwayRoadmap,
  getRoadmapSummary,
  updateRoadmapProgress
} from '../controllers/roadmap.controller.js'

const router = Router()

router.use(authenticate)

/**
 * @swagger
 * /roadmap/summary:
 *   get:
 *     summary: Get roadmap summary for all user's started pathways
 *     description: Returns a list of all pathways the user has started, with overall progress for each.
 *     tags: [Roadmap]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Roadmap summary retrieved successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 message:
 *                   type: string
 *                   example: Roadmap summary retrieved
 *                 data:
 *                   type: object
 *                   properties:
 *                     summary:
 *                       type: array
 *                       items:
 *                         type: object
 *                         properties:
 *                           pathwaySlug:
 *                             type: string
 *                             example: sports-coaching
 *                           pathwayTitle:
 *                             type: string
 *                             example: Sports Coaching
 *                           overallProgress:
 *                             type: integer
 *                             minimum: 0
 *                             maximum: 100
 *                             example: 40
 *                           lastActivityAt:
 *                             type: string
 *                             format: date-time
 *                             example: 2026-03-24T03:15:00.000Z
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/summary', getRoadmapSummary as any)

/**
 * @swagger
 * /roadmap/pathway/{slug}:
 *   get:
 *     summary: Get personalised roadmap for a specific pathway
 *     description: Returns the full milestone roadmap for the given pathway, merged with the user's current progress.
 *     tags: [Roadmap]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: slug
 *         required: true
 *         schema:
 *           type: string
 *         example: sports-coaching
 *     responses:
 *       200:
 *         description: Roadmap retrieved successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 message:
 *                   type: string
 *                   example: Roadmap retrieved
 *                 data:
 *                   type: object
 *                   properties:
 *                     roadmap:
 *                       type: object
 *                       properties:
 *                         pathwaySlug:
 *                           type: string
 *                           example: sports-coaching
 *                         pathwayTitle:
 *                           type: string
 *                           example: Sports Coaching
 *                         timeToEntry:
 *                           type: string
 *                           example: 6-12 months
 *                         overallProgress:
 *                           type: integer
 *                           minimum: 0
 *                           maximum: 100
 *                           example: 25
 *                         startedAt:
 *                           type: string
 *                           format: date-time
 *                         lastActivityAt:
 *                           type: string
 *                           format: date-time
 *                         milestones:
 *                           type: array
 *                           items:
 *                             type: object
 *                             properties:
 *                               id:
 *                                 type: string
 *                                 example: milestone-1
 *                               title:
 *                                 type: string
 *                                 example: Complete coaching certification
 *                               description:
 *                                 type: string
 *                               type:
 *                                 type: string
 *                                 example: certification
 *                               duration:
 *                                 type: string
 *                                 example: 3 months
 *                               estimatedCost:
 *                                 type: string
 *                                 example: $500
 *                               status:
 *                                 type: string
 *                                 enum: [not_started, in_progress, completed]
 *                                 example: in_progress
 *                               completedAt:
 *                                 type: string
 *                                 format: date-time
 *                               notes:
 *                                 type: string
 *                               resources:
 *                                 type: array
 *                                 items:
 *                                   type: object
 *                                   properties:
 *                                     name:
 *                                       type: string
 *                                     url:
 *                                       type: string
 *                                       format: uri
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       404:
 *         description: Roadmap not found for the given pathway slug
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/pathway/:slug', getPathwayRoadmap as any)

/**
 * @swagger
 * /roadmap/pathway/{slug}/progress:
 *   post:
 *     summary: Update roadmap milestone progress
 *     tags: [Roadmap]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: slug
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - milestoneId
 *               - milestoneTitle
 *               - status
 *             properties:
 *               milestoneId:
 *                 type: string
 *               milestoneTitle:
 *                 type: string
 *                 maxLength: 200
 *               status:
 *                 type: string
 *                 enum: [not_started, in_progress, completed]
 *               notes:
 *                 type: string
 *                 maxLength: 1000
 *     responses:
 *       200:
 *         description: Milestone progress updated
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiSuccessResponse'
 *       400:
 *         description: Invalid request payload
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       401:
 *         description: Unauthorized
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.post('/pathway/:slug/progress', validate(roadmapProgressSchema), updateRoadmapProgress as any)

export default router
