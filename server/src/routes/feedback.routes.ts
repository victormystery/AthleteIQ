import { Router } from 'express'
import { authenticate } from '../middleware/auth.middleware.js'
import { validate } from '../middleware/validate.middleware.js'
import { feedbackSchema } from '../validators/feedback.validator.js'
import { submitFeedback, getMyFeedback } from '../controllers/feedback.controller.js'

const router = Router()

router.use(authenticate)

/**
 * @swagger
 * /feedback:
 *   post:
 *     summary: Submit feedback for a recommendation
 *     tags: [Feedback]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - recommendationId
 *               - pathwaySlug
 *               - rating
 *               - interested
 *             properties:
 *               recommendationId:
 *                 type: string
 *                 pattern: '^[a-fA-F0-9]{24}$'
 *               pathwaySlug:
 *                 type: string
 *               rating:
 *                 type: integer
 *                 minimum: 1
 *                 maximum: 5
 *               interested:
 *                 type: boolean
 *               comment:
 *                 type: string
 *                 maxLength: 1000
 *     responses:
 *       200:
 *         description: Feedback submitted
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
router.post('/', validate(feedbackSchema), submitFeedback as any)

/**
 * @swagger
 * /feedback/my:
 *   get:
 *     summary: Get current user's feedback history
 *     description: Returns all recommendation feedback submitted by the authenticated user, sorted newest first.
 *     tags: [Feedback]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Feedback history retrieved successfully
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
 *                   example: Feedback history retrieved
 *                 data:
 *                   type: object
 *                   properties:
 *                     feedback:
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
 *                           recommendation:
 *                             type: string
 *                             example: 65f7a6f5d2a8f8b6b85f0002
 *                           pathwaySlug:
 *                             type: string
 *                             example: sports-coaching
 *                           rating:
 *                             type: integer
 *                             minimum: 1
 *                             maximum: 5
 *                             example: 4
 *                           interested:
 *                             type: boolean
 *                             example: true
 *                           comment:
 *                             type: string
 *                             example: Great recommendation, very relevant to my goals.
 *                           createdAt:
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
router.get('/my', getMyFeedback as any)

export default router
