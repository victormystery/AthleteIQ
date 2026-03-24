import { Router } from 'express'
import { authenticate } from '../middleware/auth.middleware.js'
import { validate } from '../middleware/validate.middleware.js'
import { questionnaireSchema } from '../validators/questionnaire.validator.js'
import {
  submitQuestionnaire,
  getMyQuestionnaires
} from '../controllers/questionnaire.controller.js'

const router = Router()

router.use(authenticate)

/**
 * @swagger
 * /questionnaire:
 *   post:
 *     summary: Submit questionnaire and get career recommendations
 *     tags: [Questionnaire]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - academic_level
 *               - primary_sport
 *               - participation_years
 *               - participation_level
 *               - fitness_level
 *               - technical_skill
 *               - leadership
 *               - data_comfort
 *               - motivation
 *               - career_importance
 *               - work_environment
 *               - biggest_challenge
 *               - injury_history
 *               - career_interests
 *             properties:
 *               academic_level:
 *                 type: string
 *                 enum:
 *                   - Year 1
 *                   - Year 2
 *                   - Year 3
 *                   - Year 4
 *                   - Postgraduate
 *                   - Professional
 *               primary_sport:
 *                 type: string
 *                 minLength: 2
 *                 maxLength: 100
 *               participation_years:
 *                 type: string
 *                 enum:
 *                   - "< 1"
 *                   - 1-2
 *                   - 3-5
 *                   - "> 5"
 *               participation_level:
 *                 type: string
 *                 enum:
 *                   - Not active
 *                   - Recreational
 *                   - Club
 *                   - Regional
 *                   - National
 *                   - Elite
 *               fitness_level:
 *                 type: integer
 *                 minimum: 1
 *                 maximum: 5
 *               technical_skill:
 *                 type: integer
 *                 minimum: 1
 *                 maximum: 5
 *               leadership:
 *                 type: integer
 *                 minimum: 1
 *                 maximum: 5
 *               data_comfort:
 *                 type: integer
 *                 minimum: 1
 *                 maximum: 5
 *               motivation:
 *                 type: string
 *                 enum:
 *                   - Competition
 *                   - Health
 *                   - Coaching
 *                   - Academic
 *                   - Fame
 *               career_importance:
 *                 type: string
 *                 enum:
 *                   - Financial security
 *                   - "Passion & purpose"
 *                   - Work-life balance
 *                   - Career progression
 *                   - Social impact
 *               work_environment:
 *                 type: string
 *                 enum:
 *                   - Field
 *                   - Office
 *                   - Lab
 *                   - Media
 *                   - Mixed
 *               biggest_challenge:
 *                 type: string
 *                 enum:
 *                   - Lack of experience
 *                   - Academic pressure
 *                   - Financial constraints
 *                   - "Injury & health"
 *                   - Networking gaps
 *                   - Unclear goals
 *               injury_history:
 *                 type: string
 *                 enum:
 *                   - No injuries
 *                   - Minor injuries
 *                   - Significant injuries
 *                   - Career-limiting injury
 *               career_interests:
 *                 type: array
 *                 minItems: 1
 *                 maxItems: 3
 *                 items:
 *                   type: string
 *     responses:
 *       201:
 *         description: Questionnaire submitted and recommendations generated
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
router.post('/', validate(questionnaireSchema), submitQuestionnaire as any)

/**
 * @swagger
 * /questionnaire/my:
 *   get:
 *     summary: Get current user's questionnaire history
 *     description: Returns all questionnaire submissions for the authenticated user, sorted newest first.
 *     tags: [Questionnaire]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Questionnaire history retrieved successfully
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
 *                   example: Questionnaire history retrieved
 *                 data:
 *                   type: object
 *                   properties:
 *                     responses:
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
 *                           academic_level:
 *                             type: string
 *                             enum: [Year 1, Year 2, Year 3, Year 4, Postgraduate, Professional]
 *                             example: Year 3
 *                           primary_sport:
 *                             type: string
 *                             example: Football
 *                           participation_years:
 *                             type: string
 *                             enum: ["< 1", "1-2", "3-5", "> 5"]
 *                             example: 3-5
 *                           participation_level:
 *                             type: string
 *                             enum: [Not active, Recreational, Club, Regional, National, Elite]
 *                             example: Regional
 *                           fitness_level:
 *                             type: integer
 *                             minimum: 1
 *                             maximum: 5
 *                             example: 4
 *                           technical_skill:
 *                             type: integer
 *                             minimum: 1
 *                             maximum: 5
 *                             example: 3
 *                           leadership:
 *                             type: integer
 *                             minimum: 1
 *                             maximum: 5
 *                             example: 4
 *                           data_comfort:
 *                             type: integer
 *                             minimum: 1
 *                             maximum: 5
 *                             example: 2
 *                           motivation:
 *                             type: string
 *                             enum: [Competition, Health, Coaching, Academic, Fame]
 *                             example: Coaching
 *                           career_importance:
 *                             type: string
 *                             enum: [Financial security, "Passion & purpose", Work-life balance, Career progression, Social impact]
 *                             example: Passion & purpose
 *                           work_environment:
 *                             type: string
 *                             enum: [Field, Office, Lab, Media, Mixed]
 *                             example: Field
 *                           biggest_challenge:
 *                             type: string
 *                             enum: [Lack of experience, Academic pressure, Financial constraints, "Injury & health", Networking gaps, Unclear goals]
 *                             example: Networking gaps
 *                           injury_history:
 *                             type: string
 *                             enum: [No injuries, Minor injuries, Significant injuries, Career-limiting injury]
 *                             example: Minor injuries
 *                           career_interests:
 *                             type: array
 *                             items:
 *                               type: string
 *                             example: [Sports Coaching, Sports Analytics]
 *                           submittedAt:
 *                             type: string
 *                             format: date-time
 *                             example: 2026-03-24T03:15:00.000Z
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
router.get('/my', getMyQuestionnaires as any)

export default router
