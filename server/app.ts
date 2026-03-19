import express, { type Express } from 'express'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import mongoSanitize from 'express-mongo-sanitize'
import swaggerUi from 'swagger-ui-express'
import { env } from './src/config/env.js'
import { swaggerSpec } from './src/config/swagger.js'
import routes from './src/routes/index.js'
import { apiLimiter } from './src/middleware/rateLimit.middleware.js'
import { errorHandler, notFoundHandler } from './src/middleware/error.middleware.js'

const app: Express = express()

// Security headers
app.use(helmet())

// CORS
app.use(cors({
  origin: (origin, callback) => {
    if (!origin || env.allowedOrigins.includes(origin)) {
      callback(null, true)
    } else {
      callback(new Error('Not allowed by CORS'))
    }
  },
  credentials: true
}))

// Body parsing
app.use(express.json({ limit: '10kb' }))
app.use(express.urlencoded({ extended: true, limit: '10kb' }))

// NoSQL injection sanitization
app.use(mongoSanitize())

// HTTP request logging
app.use(morgan(env.isDev ? 'dev' : 'combined'))

// Rate limiting on all API routes
app.use('/api', apiLimiter)

// Health check
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', env: env.nodeEnv, timestamp: new Date().toISOString() })
})

// Swagger docs
app.use('/api/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, {
  customSiteTitle: 'AthleteIQ API Docs'
}))

// API routes
app.use('/api', routes)

// 404 and error handlers
app.use(notFoundHandler)
app.use(errorHandler)

export default app
