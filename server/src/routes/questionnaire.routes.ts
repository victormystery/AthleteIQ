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
 *               - education_training_level
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
 *               primary_sport:
 *                 type: string
 *                 minLength: 2
 *                 maxLength: 100
 *               participation_years:
 *                 type: string
 *                 enum:
 *                   - Less than 1 year
 *                   - 1-2 years
 *                   - 3-5 years
 *                   - More than 5 years
 *               participation_level:
 *                 type: string
 *                 enum:
 *                   - Not active
 *                   - Recreational
 *                   - University/School team
 *                   - Club or academy
 *                   - Elite/competitive pathway
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
 *                   - Competition and performance
 *                   - Health and fitness
 *                   - Helping or coaching others
 *                   - Academic or career opportunity
 *                   - Fame, media, or recognition
 *               career_importance:
 *                 type: string
 *                 enum:
 *                   - Not important
 *                   - Slightly important
 *                   - Moderately important
 *                   - Very important
 *                   - My main career focus
 *               work_environment:
 *                 type: string
 *                 enum:
 *                   - On-field / practical
 *                   - Office / management
 *                   - Laboratory / science / clinical
 *                   - Media / creative
 *                   - A mix of environments
 *               education_training_level:
 *                 type: string
 *                 enum:
 *                   - Short courses or certifications only
 *                   - Diploma
 *                   - Bachelor's degree or add-on program
 *                   - Master's degree
 *                   - Medical/clinical or doctoral pathway
 *               biggest_challenge:
 *                 type: string
 *                 enum:
 *                   - Academic workload
 *                   - Time management
 *                   - Financial constraints
 *                   - Injury risk or health
 *                   - Lack of facilities or coaching
 *                   - Motivation
 *               injury_history:
 *                 type: string
 *                 enum:
 *                   - None
 *                   - Minor (short recovery)
 *                   - Moderate (missed competitions)
 *                   - Severe (long-term impact)
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
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 message:
 *                   type: string
 *                   example: Questionnaire submitted and recommendations generated
 *                 data:
 *                   type: object
 *                   properties:
 *                     questionnaireResponse:
 *                       type: object
 *                       description: The saved questionnaire submission
 *                       properties:
 *                         _id:
 *                           type: string
 *                           example: 65f7a6f5d2a8f8b6b85f1123
 *                         user:
 *                           type: string
 *                           example: 65f7a6f5d2a8f8b6b85f0001
 *                         primary_sport:
 *                           type: string
 *                           example: Football
 *                         academic_level:
 *                           type: string
 *                           example: Year 3
 *                         submittedAt:
 *                           type: string
 *                           format: date-time
 *                     recommendation:
 *                       type: object
 *                       description: The ML-generated career recommendations
 *                       properties:
 *                         _id:
 *                           type: string
 *                           example: 65f7a6f5d2a8f8b6b85f2234
 *                         topRecommendation:
 *                           type: string
 *                           example: sports-coaching
 *                         mlModelVersion:
 *                           type: string
 *                           example: 1.0.0
 *                         processingTimeMs:
 *                           type: integer
 *                           example: 312
 *                         recommendations:
 *                           type: array
 *                           items:
 *                             type: object
 *                             properties:
 *                               pathwaySlug:
 *                                 type: string
 *                                 example: sports-coaching
 *                               pathwayName:
 *                                 type: string
 *                                 example: Sports Coaching
 *                               matchPercentage:
 *                                 type: integer
 *                                 example: 87
 *                               confidence:
 *                                 type: number
 *                                 format: float
 *                                 example: 0.87
 *                               rank:
 *                                 type: integer
 *                                 example: 1
 *                               keySkillsMatch:
 *                                 type: array
 *                                 items:
 *                                   type: string
 *                               sportSpecificInsights:
 *                                 type: array
 *                                 items:
 *                                   type: string
 *                               salaryRange:
 *                                 type: object
 *                                 properties:
 *                                   min:
 *                                     type: integer
 *                                     example: 35000
 *                                   max:
 *                                     type: integer
 *                                     example: 75000
 *                                   currency:
 *                                     type: string
 *                                     example: USD
 *                               jobGrowthOutlook:
 *                                 type: string
 *                                 example: Growing
 *                         motivationRecommendation:
 *                           type: object
 *                           properties:
 *                             pathwaySlug:
 *                               type: string
 *                               example: sports-coaching
 *                             pathwayName:
 *                               type: string
 *                               example: Sports Coaching
 *                             reason:
 *                               type: string
 *                               example: Aligns with your Coaching motivation
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
 *                             enum: [Year 1, Year 2, Year 3, Year 4, Postgraduate]
 *                             example: Year 3
 *                           primary_sport:
 *                             type: string
 *                             example: Football
 *                           participation_years:
 *                             type: string
 *                             enum: [Less than 1 year, 1-2 years, 3-5 years, More than 5 years]
 *                             example: 3-5 years
 *                           participation_level:
 *                             type: string
 *                             enum: [Not active, Recreational, University/School team, Club or academy, Elite/competitive pathway]
 *                             example: University/School team
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
 *                             enum: [Competition and performance, Health and fitness, Helping or coaching others, Academic or career opportunity, "Fame, media, or recognition"]
 *                             example: Helping or coaching others
 *                           career_importance:
 *                             type: string
 *                             enum: [Not important, Slightly important, Moderately important, Very important, My main career focus]
 *                             example: Very important
 *                           work_environment:
 *                             type: string
 *                             enum: ["On-field / practical", "Office / management", "Laboratory / science / clinical", "Media / creative", "A mix of environments"]
 *                             example: On-field / practical
 *                           education_training_level:
 *                             type: string
 *                             enum: [Short courses or certifications only, Diploma, "Bachelor's degree or add-on program", "Master's degree", Medical/clinical or doctoral pathway]
 *                             example: Bachelor's degree or add-on program
 *                           biggest_challenge:
 *                             type: string
 *                             enum: [Academic workload, Time management, Financial constraints, Injury risk or health, Lack of facilities or coaching, Motivation]
 *                             example: Time management
 *                           injury_history:
 *                             type: string
 *                             enum: [None, Minor (short recovery), Moderate (missed competitions), Severe (long-term impact)]
 *                             example: Minor (short recovery)
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
