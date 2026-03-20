import swaggerJsdoc from 'swagger-jsdoc'
import { env } from './env.js'

const options: swaggerJsdoc.Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'AthleteIQ API',
      version: '2.1.0',
      description:
        'Sports Career Recommender REST API — helps student-athletes discover career pathways through ML-powered recommendations.',
      contact: {
        name: 'AthleteIQ Support'
      }
    },
    servers: [
      {
        url: `http://localhost:${env.port}/api`,
        description: 'Development server'
      }
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT'
        }
      },
      schemas: {
        UserSummary: {
          type: 'object',
          properties: {
            _id: { type: 'string', example: '65f7a6f5d2a8f8b6b85f1123' },
            name: { type: 'string', example: 'Jane Athlete' },
            email: { type: 'string', format: 'email', example: 'jane@example.com' },
            role: { type: 'string', example: 'student_athlete' }
          }
        },
        AuthData: {
          type: 'object',
          required: ['token', 'user'],
          properties: {
            token: { type: 'string', example: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' },
            user: { $ref: '#/components/schemas/UserSummary' }
          }
        },
        RegisterData: {
          type: 'object',
          required: ['user'],
          properties: {
            user: { $ref: '#/components/schemas/UserSummary' }
          }
        },
        AuthSuccessResponse: {
          type: 'object',
          required: ['success', 'message', 'data'],
          properties: {
            success: { type: 'boolean', example: true },
            message: { type: 'string', example: 'Logged in successfully' },
            data: { $ref: '#/components/schemas/AuthData' }
          }
        },
        RegisterSuccessResponse: {
          type: 'object',
          required: ['success', 'message', 'data'],
          properties: {
            success: { type: 'boolean', example: true },
            message: { type: 'string', example: 'Account created successfully' },
            data: { $ref: '#/components/schemas/RegisterData' }
          }
        },
        ApiSuccessResponse: {
          type: 'object',
          required: ['success', 'message'],
          properties: {
            success: { type: 'boolean', example: true },
            message: { type: 'string', example: 'OK' },
            data: {
              type: 'object',
              additionalProperties: true,
              description: 'Endpoint-specific payload'
            }
          }
        },
        ApiErrorResponse: {
          type: 'object',
          required: ['success', 'message'],
          properties: {
            success: { type: 'boolean', example: false },
            message: { type: 'string', example: 'Invalid email or password' },
            requestId: { type: 'string', example: 'b0d95f7d-0ad2-4261-9349-b5cebe55a1b4' },
            stack: {
              type: 'string',
              description: 'Present in development mode only'
            }
          }
        }
      }
    },
    security: [{ bearerAuth: [] }],
    tags: [
      { name: 'Auth', description: 'Authentication — register and login' },
      { name: 'Profile', description: 'User profile management (authenticated regular users)' },
      { name: 'Career', description: 'Career pathways and recommendations' },
      { name: 'Questionnaire', description: 'Assessment questionnaire submission' },
      { name: 'Roadmap', description: 'Personalised career roadmaps' },
      { name: 'Feedback', description: 'Recommendation feedback' },
      { name: 'Feedback Loop', description: 'Aggregated feedback insights (career_advisor/admin only)' },
      { name: 'Progress', description: 'Milestone progress tracking' },
      { name: 'Admin', description: 'Admin dashboard (admin role only)' }
    ]
  },
  apis: ['./src/routes/*.ts']
}

export const swaggerSpec = swaggerJsdoc(options)
