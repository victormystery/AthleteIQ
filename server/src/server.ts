import app from '../app.js'
import { env } from './config/env.js'
import { connectDB } from './config/db.js'
import { initBetterAuth } from './config/betterAuth.js'
import { googleSheetsService } from './services/googleSheets.service.js'
import { logger } from './utils/logger.js'
import { CareerPathway, User } from './models/index.js'
import { careerPathwaysSeedData } from './data/career_pathways.js'
import mongoose from 'mongoose'

// ── Process-level exception handlers ───────────────────────────────────────
// These catch errors that escape Express (e.g. async code outside a route
// or a synchronous throw in a module). Without them, the process crashes
// silently with no structured log entry.

process.on('uncaughtException', (err: Error) => {
  logger.error('Uncaught exception — shutting down', {
    error: err.message,
    stack: err.stack
  })
  // Allow the logger to flush before exiting
  process.exit(1)
})

process.on('unhandledRejection', (reason: unknown) => {
  const message = reason instanceof Error ? reason.message : String(reason)
  const stack = reason instanceof Error ? reason.stack : undefined
  logger.error('Unhandled promise rejection — shutting down', { error: message, stack })
  process.exit(1)
})

// ── Auto-seed ───────────────────────────────────────────────────────────────
async function autoSeed(): Promise<void> {
  const count = await CareerPathway.countDocuments()
  if (count > 0) return

  logger.info('No career pathways found — seeding database...')
  for (const pathway of careerPathwaysSeedData) {
    await CareerPathway.updateOne({ slug: pathway.slug }, pathway, { upsert: true })
  }
  logger.info(`Seeded ${careerPathwaysSeedData.length} career pathways`)

  const adminEmail = 'admin@athleteiq.com'
  const adminExists = await User.findOne({ email: adminEmail })
  if (!adminExists) {
    await User.create({
      name: 'AthleteIQ Admin',
      email: adminEmail,
      password: 'Admin@AthleteIQ2026!',
      role: 'admin'
    })
    logger.info('Admin user created')
  }
}

// ── Startup ─────────────────────────────────────────────────────────────────
async function start(): Promise<void> {
  await connectDB()
  if (!mongoose.connection.db) {
    throw new Error('MongoDB connection is not ready for BetterAuth initialization')
  }
  initBetterAuth(mongoose.connection.db)
  googleSheetsService.validateConfig()
  await autoSeed()

  const server = app.listen(env.port, () => {
    logger.info(`Server running on port ${env.port}`, {
      env: env.nodeEnv,
      logLevel: env.logLevel
    })
  })

  // ── Graceful shutdown ──────────────────────────────────────────────────────
  // On SIGTERM/SIGINT (PM2, Docker, Kubernetes) stop accepting new connections
  // and wait for in-flight requests to finish before exiting.
  const shutdown = (signal: string) => {
    logger.info(`${signal} received — closing HTTP server gracefully`)
    server.close(() => {
      logger.info('HTTP server closed')
      process.exit(0)
    })
  }

  process.on('SIGTERM', () => shutdown('SIGTERM'))
  process.on('SIGINT', () => shutdown('SIGINT'))
}

start().catch((err: Error) => {
  // Use logger so the startup failure appears in the same structured format
  // as all other logs — avoids a plain console.error breaking JSON log pipelines.
  logger.error('Failed to start server', { error: err.message, stack: err.stack })
  process.exit(1)
})
