import { Router } from 'express'
import { authenticate } from '../middleware/auth.middleware.js'
import { adminOnly } from '../middleware/rbac.middleware.js'
import {
  getDashboardStats,
  listUsers,
  getRecentAssessments,
  deleteUser,
  suspendUser,
  updateUserRole
} from '../controllers/admin.controller.js'

const router = Router()

// All admin routes require authentication + admin role
router.use(authenticate, adminOnly)

/**
 * @swagger
 * /admin/stats:
 *   get:
 *     summary: Get admin dashboard statistics
 *     description: "Access: Admin users only."
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Admin dashboard data retrieved successfully
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
 *                   example: Admin dashboard data retrieved
 *                 data:
 *                   type: object
 *                   properties:
 *                     stats:
 *                       type: object
 *                       properties:
 *                         totalUsers:
 *                           type: integer
 *                           example: 250
 *                         totalStudents:
 *                           type: integer
 *                           example: 210
 *                         totalAdvisors:
 *                           type: integer
 *                           example: 15
 *                         totalAssessments:
 *                           type: integer
 *                           example: 180
 *                         totalFeedback:
 *                           type: integer
 *                           example: 95
 *                     recentUsers:
 *                       type: array
 *                       description: 10 most recently registered users
 *                       items:
 *                         $ref: '#/components/schemas/UserSummary'
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       403:
 *         description: Forbidden — admin role required
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/stats', getDashboardStats)

/**
 * @swagger
 * /admin/users:
 *   get:
 *     summary: List all users (paginated)
 *     description: "Access: Admin users only."
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           default: 1
 *         description: Page number (default 1)
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           default: 20
 *         description: Results per page (max 100, default 20)
 *     responses:
 *       200:
 *         description: Users retrieved successfully
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
 *                   example: Users retrieved
 *                 data:
 *                   type: object
 *                   properties:
 *                     users:
 *                       type: array
 *                       items:
 *                         $ref: '#/components/schemas/UserSummary'
 *                     pagination:
 *                       type: object
 *                       properties:
 *                         page:
 *                           type: integer
 *                           example: 1
 *                         limit:
 *                           type: integer
 *                           example: 20
 *                         total:
 *                           type: integer
 *                           example: 250
 *                         pages:
 *                           type: integer
 *                           example: 13
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       403:
 *         description: Forbidden — admin role required
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/users', listUsers)

/**
 * @swagger
 * /admin/assessments:
 *   get:
 *     summary: Get recent assessments across all users
 *     description: "Access: Admin users only."
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           default: 20
 *         description: Max number of assessments to return (max 50, default 20)
 *     responses:
 *       200:
 *         description: Recent assessments retrieved successfully
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
 *                   example: Recent assessments retrieved
 *                 data:
 *                   type: object
 *                   properties:
 *                     assessments:
 *                       type: array
 *                       items:
 *                         type: object
 *                         properties:
 *                           _id:
 *                             type: string
 *                             example: 65f7a6f5d2a8f8b6b85f1123
 *                           user:
 *                             type: object
 *                             properties:
 *                               name:
 *                                 type: string
 *                                 example: Jane Athlete
 *                               email:
 *                                 type: string
 *                                 example: jane@example.com
 *                               role:
 *                                 type: string
 *                                 example: student
 *                           questionnaireResponse:
 *                             type: object
 *                             properties:
 *                               primary_sport:
 *                                 type: string
 *                                 example: Football
 *                               academic_level:
 *                                 type: string
 *                                 example: Year 3
 *                           topRecommendation:
 *                             type: string
 *                             example: sports-coaching
 *                           createdAt:
 *                             type: string
 *                             format: date-time
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       403:
 *         description: Forbidden — admin role required
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.get('/assessments', getRecentAssessments)

/**
 * @swagger
 * /admin/users/{id}:
 *   delete:
 *     summary: Delete a user by ID
 *     description: "Access: Admin users only."
 *     tags: [Admin]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         example: 65f7a6f5d2a8f8b6b85f0001
 *     responses:
 *       200:
 *         description: User deleted successfully
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
 *                   example: User deleted successfully
 *                 data:
 *                   nullable: true
 *                   example: null
 *       401:
 *         description: Unauthorized — missing or invalid token
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       403:
 *         description: Forbidden — admin role required
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 *       404:
 *         description: User not found
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ApiErrorResponse'
 */
router.delete('/users/:id', deleteUser)

router.patch('/users/:id/suspend', suspendUser)

router.patch('/users/:id/role', updateUserRole)

export default router
