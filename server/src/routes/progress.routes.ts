import { Router } from 'express'
import { authenticate } from '../middleware/auth.middleware.js'
import { validate } from '../middleware/validate.middleware.js'
import { progressSchema } from '../validators/progress.validator.js'
import { upsertProgress, getMyProgress } from '../controllers/progress.controller.js'

const router = Router()

router.use(authenticate)

/**
 * @swagger
 * /progress:
 *   post:
 *     summary: Create or update milestone progress
 *     tags: [Progress]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - pathwaySlug
 *               - milestoneId
 *               - milestoneTitle
 *               - status
 *             properties:
 *               pathwaySlug:
 *                 type: string
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
 *         description: Progress updated
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
router.post('/', validate(progressSchema), upsertProgress as any)

/**
 * @swagger
 * /progress/my-progress:
 *   get:
 *     summary: Get all progress records for the current user
 *     description: Returns one progress record per pathway the user has started, including all milestone statuses.
 *     tags: [Progress]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Progress records retrieved successfully
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
 *                   example: Progress records retrieved
 *                 data:
 *                   type: object
 *                   properties:
 *                     progress:
 *                       type: array
 *                       items:
 *                         type: object
 *                         properties:
 *                           _id:
 *                             type: string
 *                             example: 65f7a6f5d2a8f8b6b85f1123
 *                           user:
 *                             type: string
 *                             example: 65f7a6f5d2a8f8b6b85f0001
 *                           pathwaySlug:
 *                             type: string
 *                             example: sports-coaching
 *                           overallProgress:
 *                             type: integer
 *                             minimum: 0
 *                             maximum: 100
 *                             example: 50
 *                           startedAt:
 *                             type: string
 *                             format: date-time
 *                           lastActivityAt:
 *                             type: string
 *                             format: date-time
 *                           milestones:
 *                             type: array
 *                             items:
 *                               type: object
 *                               properties:
 *                                 milestoneId:
 *                                   type: string
 *                                   example: milestone-1
 *                                 title:
 *                                   type: string
 *                                   example: Complete coaching certification
 *                                 status:
 *                                   type: string
 *                                   enum: [not_started, in_progress, completed]
 *                                   example: completed
 *                                 completedAt:
 *                                   type: string
 *                                   format: date-time
 *                                 notes:
 *                                   type: string
 *                                   example: Passed with distinction
 *                                 updatedAt:
 *                                   type: string
 *                                   format: date-time
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/my-progress', getMyProgress as any)

export default router
