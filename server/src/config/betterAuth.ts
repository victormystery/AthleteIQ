import { betterAuth } from 'better-auth'
import { fromNodeHeaders, toNodeHandler } from 'better-auth/node'
import { mongodbAdapter } from '@better-auth/mongo-adapter'
import type { Request, Response, NextFunction } from 'express'
import type { Db } from 'mongodb'
import { env } from './env.js'
import { logger } from '../utils/logger.js'

let authInstance: ReturnType<typeof betterAuth> | null = null

function buildTrustedOrigins(): string[] {
  // Include serverUrl so BetterAuth accepts our own /api/auth/google/callback as a valid callbackURL
  const origins = new Set<string>([env.clientUrl, env.serverUrl, ...env.allowedOrigins])
  return Array.from(origins)
}

export function initBetterAuth(db: Db): void {
  const enableGoogle = Boolean(env.googleClientId && env.googleClientSecret)

  authInstance = betterAuth({
    baseURL: env.serverUrl,
    // IMPORTANT: basePath must match the Express mount point in app.ts (`app.all('/api/bauth/*', ...)`)
    // BetterAuth constructs its own redirect_uri as: baseURL + basePath + '/callback/google'
    // If basePath doesn't match the mount, Google redirects to an unreachable URL → Error 400
    basePath: '/api/bauth',
    secret: env.betterAuthSecret,
    trustedOrigins: buildTrustedOrigins(),
    database: mongodbAdapter(db, {
      transaction: false
    }),
    socialProviders: enableGoogle
      ? {
          google: {
            clientId: env.googleClientId as string,
            clientSecret: env.googleClientSecret as string,
            prompt: 'select_account'
          }
        }
      : undefined
  }) as ReturnType<typeof betterAuth>

  if (!enableGoogle) {
    logger.warn('BetterAuth Google OAuth disabled — GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET missing')
  }
}

export function getBetterAuth() {
  if (!authInstance) {
    throw new Error('BetterAuth is not initialized. Call initBetterAuth() after MongoDB connects.')
  }
  return authInstance
}

export async function betterAuthHandler(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const auth = getBetterAuth()
    const handler = toNodeHandler(auth)
    await handler(req, res)
  } catch (err) {
    next(err)
  }
}

export { fromNodeHeaders }
