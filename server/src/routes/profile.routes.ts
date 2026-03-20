import { Router } from 'express'
import { authenticate } from '../middleware/auth.middleware.js'
import { validate } from '../middleware/validate.middleware.js'
import { updateProfileSchema } from '../validators/profile.validator.js'
import { getMyProfile, updateMyProfile } from '../controllers/profile.controller.js'

const router = Router()

router.use(authenticate)

/**
 * @swagger
 * /profile/me:
 *   get:
 *     summary: Get current user profile
 *     description: "Access: Authenticated users (regular users)."
 *     tags: [Profile]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Profile retrieved successfully
 */
router.get('/me', getMyProfile as any)

/**
 * @swagger
 * /profile/me:
 *   put:
 *     summary: Update current user profile
 *     description: "Access: Authenticated users (regular users)."
 *     tags: [Profile]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               university:
 *                 type: string
 *                 maxLength: 200
 *               programOfStudy:
 *                 type: string
 *                 maxLength: 200
 *               primarySport:
 *                 type: string
 *                 maxLength: 100
 *               yearOfStudy:
 *                 type: string
 *                 enum: [Year 1, Year 2, Year 3, Year 4, Postgraduate, Professional, ""]
 *               avatarUrl:
 *                 type: string
 *                 format: uri
 *               bio:
 *                 type: string
 *                 maxLength: 500
 *     responses:
 *       200:
 *         description: Profile updated
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
router.put('/me', validate(updateProfileSchema), updateMyProfile as any)

export default router
