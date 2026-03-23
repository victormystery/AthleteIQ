import { Router } from 'express'
import { authenticate } from '../middleware/auth.middleware.js'
import {
  listPathways,
  getPathway,
  getRecommendations,
  getHistory
} from '../controllers/career.controller.js'

const router = Router()

/**
 * @swagger
 * /career/pathways:
 *   get:
 *     summary: List all career pathways
 *     tags: [Career]
 *     responses:
 *       200:
 *         description: List of active career pathways
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiSuccessResponse'
 *       500:
 *         description: Server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/pathways', listPathways)

/**
 * @swagger
 * /career/pathways/{slug}:
 *   get:
 *     summary: Get a specific career pathway by slug
 *     tags: [Career]
 *     parameters:
 *       - in: path
 *         name: slug
 *         required: true
 *         schema:
 *           type: string
 *         example: coaching-development
 *     responses:
 *       200:
 *         description: Career pathway details
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiSuccessResponse'
 *       404:
 *         description: Pathway not found
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       500:
 *         description: Server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/pathways/:slug', getPathway)

// Protected routes
router.use(authenticate)

/**
 * @swagger
 * /career/recommendations:
 *   get:
 *     summary: Get user's saved recommendations
 *     tags: [Career]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: User's most recent career recommendations (up to 10)
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiSuccessResponse'
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       500:
 *         description: Server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/recommendations', getRecommendations as any)

/**
 * @swagger
 * /career/history:
 *   get:
 *     summary: Get user's full assessment history
 *     tags: [Career]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Full list of the user's career assessment history
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiSuccessResponse'
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       500:
 *         description: Server error
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/history', getHistory as any)

export default router
