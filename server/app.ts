import express, { type Express } from 'express'
import cors from 'cors'
import helmet from 'helmet'
import morgan from 'morgan'
import mongoSanitize from 'express-mongo-sanitize'
import swaggerUi from 'swagger-ui-express'
import { env } from './src/config/env.js'
import { swaggerSpec } from './src/config/swagger.js'
import { morganStream } from './src/utils/logger.js'
import { requestId } from './src/middleware/requestId.middleware.js'
import { betterAuthHandler } from './src/config/betterAuth.js'
import routes from './src/routes/index.js'
import { apiLimiter } from './src/middleware/rateLimit.middleware.js'
import { errorHandler, notFoundHandler } from './src/middleware/error.middleware.js'

const app: Express = express()

// ── Trust Render's reverse proxy so express-rate-limit reads the correct IP ──
app.set('trust proxy', 1)

const localhostHosts = new Set(['localhost', '127.0.0.1', '::1', '[::1]'])

function isAllowedDevOrigin(origin: string): boolean {
  if (!env.isDev) return false
  try {
    const parsed = new URL(origin)
    return localhostHosts.has(parsed.hostname)
  } catch {
    return false
  }
}

// ── Request ID — must be first so all downstream middleware can use req.id ──
app.use(requestId)

// ── Security headers ────────────────────────────────────────────────────────
app.use(helmet())

// ── CORS ────────────────────────────────────────────────────────────────────
app.use(cors({
  origin: (origin, callback) => {
    if (!origin) {
      callback(null, true)
      return
    }

    if (env.allowedOrigins.includes(origin) || isAllowedDevOrigin(origin)) {
      callback(null, true)
    } else {
      // Reject cross-origin browser access without throwing a server error.
      callback(null, false)
    }
  },
  credentials: true
}))

// ── BetterAuth routes (must run before express.json) ───────────────────────
app.all('/api/bauth/*', betterAuthHandler)

// ── Body parsing ────────────────────────────────────────────────────────────
app.use(express.json({ limit: '10kb' }))
app.use(express.urlencoded({ extended: true, limit: '10kb' }))

// ── NoSQL injection sanitization ────────────────────────────────────────────
app.use(mongoSanitize())

// ── HTTP request logging via Winston ────────────────────────────────────────
// Morgan pipes every access log line into logger.http() so HTTP and
// application logs share the same transport chain (console + file in prod).
app.use(morgan('combined', { stream: morganStream }))

// ── Rate limiting ───────────────────────────────────────────────────────────
app.use('/api', apiLimiter)

// ── Root ─────────────────────────────────────────────────────────────────────
app.get('/', (_req, res) => {
  res.json({ name: 'AthleteIQ API', docs: '/api/docs', health: '/health' })
})

// ── Health check ─────────────────────────────────────────────────────────────
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', env: env.nodeEnv, timestamp: new Date().toISOString() })
})

// ── Swagger docs ────────────────────────────────────────────────────────────
app.use('/api/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, {
  customSiteTitle: 'AthleteIQ API Docs'
}))

// ── API routes ───────────────────────────────────────────────────────────────
app.use('/api', routes)

// ── 404 and error handlers ──────────────────────────────────────────────────
app.use(notFoundHandler)
app.use(errorHandler)

export default app
