import { Router } from 'express'
import { authenticate } from '../middleware/auth.middleware.js'
import { advisorOrAdmin } from '../middleware/rbac.middleware.js'
import { getInsights, getPathwayBreakdown } from '../controllers/feedbackLoop.controller.js'

const router = Router()

// Feedback loop routes are accessible to career_advisors and admins
router.use(authenticate, advisorOrAdmin)

/**
 * @swagger
 * /feedback-loop/insights:
 *   get:
 *     summary: Get aggregated feedback insights (advisor/admin)
 *     description: "Access: Career advisor or admin users."
 *     tags: [Feedback Loop]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Feedback loop insights retrieved successfully
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
 *                   example: Feedback loop insights retrieved
 *                 data:
 *                   type: object
 *                   properties:
 *                     insights:
 *                       type: object
 *                       properties:
 *                         totalSubmissions:
 *                           type: integer
 *                           example: 120
 *                         totalFeedback:
 *                           type: integer
 *                           example: 95
 *                         averageRatingOverall:
 *                           type: number
 *                           format: float
 *                           example: 3.87
 *                         topRatedPathway:
 *                           type: string
 *                           example: sports-analytics
 *                         mostInterestingPathway:
 *                           type: string
 *                           example: sports-coaching
 *                         generatedAt:
 *                           type: string
 *                           format: date-time
 *                         pathwaySummaries:
 *                           type: array
 *                           items:
 *                             type: object
 *                             properties:
 *                               pathwaySlug:
 *                                 type: string
 *                                 example: sports-coaching
 *                               totalFeedback:
 *                                 type: integer
 *                                 example: 30
 *                               averageRating:
 *                                 type: number
 *                                 format: float
 *                                 example: 4.1
 *                               interestedCount:
 *                                 type: integer
 *                                 example: 22
 *                               notInterestedCount:
 *                                 type: integer
 *                                 example: 8
 *                               interestedRate:
 *                                 type: integer
 *                                 description: Percentage of users interested (0-100)
 *                                 example: 73
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       403:
 *         description: Forbidden — advisor or admin role required
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/insights', getInsights)

/**
 * @swagger
 * /feedback-loop/pathway/{slug}:
 *   get:
 *     summary: Get feedback breakdown for a specific pathway (advisor/admin)
 *     description: "Access: Career advisor or admin users."
 *     tags: [Feedback Loop]
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
 *         description: Pathway feedback breakdown retrieved (breakdown is null if no feedback exists yet)
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
 *                   example: Pathway feedback breakdown retrieved
 *                 data:
 *                   type: object
 *                   properties:
 *                     breakdown:
 *                       nullable: true
 *                       type: object
 *                       properties:
 *                         pathwaySlug:
 *                           type: string
 *                           example: sports-coaching
 *                         totalFeedback:
 *                           type: integer
 *                           example: 30
 *                         averageRating:
 *                           type: number
 *                           format: float
 *                           example: 4.1
 *                         interestedCount:
 *                           type: integer
 *                           example: 22
 *                         notInterestedCount:
 *                           type: integer
 *                           example: 8
 *                         interestedRate:
 *                           type: integer
 *                           description: Percentage of users interested (0-100)
 *                           example: 73
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       403:
 *         description: Forbidden — advisor or admin role required
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/pathway/:slug', getPathwayBreakdown)

export default router
