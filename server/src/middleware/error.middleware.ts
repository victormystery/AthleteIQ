import type { Request, Response, NextFunction } from 'express'
import { env } from '../config/env.js'
import { logger } from '../utils/logger.js'
import { AppError } from '../utils/errors.js'

export function errorHandler(
  err: Error | AppError,
  req: Request,
  res: Response,
  _next: NextFunction
): void {
  const statusCode = err instanceof AppError ? err.statusCode : 500
  const isOperational = err instanceof AppError ? err.isOperational : false
  const message = isOperational ? err.message : 'Internal server error'

  // Structured context attached to every log line for this error
  const logContext = {
    requestId: req.id,
    method: req.method,
    url: req.originalUrl,
    statusCode,
    ip: req.ip,
    ...(err.stack && { stack: err.stack })
  }

  if (statusCode >= 500) {
    // 5xx — programmer errors, unexpected failures
    logger.error(err.message, logContext)
  } else {
    // 4xx — operational errors: auth failures, validation, not-found
    // Logged as warn so they're visible in production without drowning error alerts
    logger.warn(err.message, logContext)
  }

  res.status(statusCode).json({
    success: false,
    message,
    // Return request ID so clients can quote it in support/bug reports
    requestId: req.id,
    ...(env.isDev && { stack: err.stack })
  })
}

export function notFoundHandler(req: Request, res: Response, next: NextFunction): void {
  // Silently discard non-API requests in development (e.g. browser tabs or HMR
  // connections from other projects accidentally hitting this API server).
  if (env.isDev && !req.originalUrl.startsWith('/api') && req.originalUrl !== '/health') {
    res.status(404).json({ success: false, message: 'Not found' })
    return
  }
  next(new AppError(`Route not found: ${req.method} ${req.originalUrl}`, 404))
}
