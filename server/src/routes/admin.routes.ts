import { Router } from 'express'
import { authenticate } from '../middleware/auth.middleware.js'
import { adminOnly } from '../middleware/rbac.middleware.js'
import {
  getDashboardStats,
  listUsers,
  getRecentAssessments,
  deleteUser
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
 *       403:
 *         description: Forbidden (admin role required)
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
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *     responses:
 *       403:
 *         description: Forbidden (admin role required)
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
 *     responses:
 *       403:
 *         description: Forbidden (admin role required)
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
 *     responses:
 *       403:
 *         description: Forbidden (admin role required)
 */
router.delete('/users/:id', deleteUser)

export default router
