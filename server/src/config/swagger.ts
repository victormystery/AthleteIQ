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
      }
    },
    security: [{ bearerAuth: [] }],
    tags: [
      { name: 'Auth', description: 'Authentication — register and login' },
      { name: 'Profile', description: 'User profile management' },
      { name: 'Career', description: 'Career pathways and recommendations' },
      { name: 'Questionnaire', description: 'Assessment questionnaire submission' },
      { name: 'Roadmap', description: 'Personalised career roadmaps' },
      { name: 'Feedback', description: 'Recommendation feedback' },
      { name: 'Feedback Loop', description: 'Aggregated feedback insights (advisor/admin)' },
      { name: 'Progress', description: 'Milestone progress tracking' },
      { name: 'Admin', description: 'Admin dashboard (admin role only)' }
    ]
  },
  apis: ['./src/routes/*.ts']
}

export const swaggerSpec = swaggerJsdoc(options)
