import type { Request, Response, NextFunction } from 'express'
import { randomBytes } from 'crypto'
import * as authService from '../services/auth.service.js'
import { success, created } from '../utils/response.js'
import { env } from '../config/env.js'
import { fromNodeHeaders, getBetterAuth } from '../config/betterAuth.js'
import GoogleAuthCode from '../models/GoogleAuthCode.model.js'
import { AppError, UnauthorizedError } from '../utils/errors.js'
import { User } from '../models/index.js'

export async function register(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const { name, email, password } = req.body as { name: string; email: string; password: string }
    const data = await authService.register(name, email, password)
    created(res, data, 'Account created successfully')
  } catch (err) {
    next(err)
  }
}

export async function login(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const { email, password } = req.body as { email: string; password: string }
    const data = await authService.login(email, password)
    success(res, data, 'Logged in successfully')
  } catch (err) {
    next(err)
  }
}

export async function startGoogleAuth(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const auth = getBetterAuth()
    const callbackURL = `${env.serverUrl}/api/auth/google/callback`
    const errorCallbackURL = `${env.clientUrl}/auth/login?error=google_failed`

    // disableRedirect: true makes BetterAuth return { url, redirect } as JSON instead of
    // issuing a 302 itself. Without it, result.response is null (no JSON body in a redirect)
    // and we cannot extract the Google OAuth URL.
    const result = await auth.api.signInSocial({
      body: {
        provider: 'google',
        callbackURL,
        newUserCallbackURL: callbackURL,
        errorCallbackURL,
        disableRedirect: true
      },
      headers: fromNodeHeaders(req.headers),
      returnHeaders: true
    })

    // Forward any state/PKCE cookie BetterAuth set so the callback can verify it
    const setCookie = result.headers?.get('set-cookie')
    if (setCookie) {
      res.setHeader('set-cookie', setCookie)
    }

    const googleUrl = result.response?.url
    if (!googleUrl) {
      throw new AppError('Unable to initiate Google sign-in', 500)
    }

    res.redirect(302, googleUrl)
  } catch (err) {
    next(err)
  }
}

export async function completeGoogleAuth(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const auth = getBetterAuth()
    const session = await auth.api.getSession({
      headers: fromNodeHeaders(req.headers)
    })

    if (!session?.user) {
      res.redirect(`${env.clientUrl}/auth/login?error=google_failed`)
      return
    }

    const email = session.user.email?.trim().toLowerCase()
    if (!email || !session.user.id) {
      res.redirect(`${env.clientUrl}/auth/login?error=google_failed`)
      return
    }

    const appUser = await authService.upsertGoogleUser({
      email,
      name: session.user.name,
      providerUserId: session.user.id
    })

    const code = randomBytes(32).toString('hex')
    const expiresAt = new Date(Date.now() + 2 * 60 * 1000)

    await GoogleAuthCode.create({
      code,
      userId: appUser._id,
      expiresAt
    })

    res.redirect(`${env.clientUrl}/auth/callback?code=${encodeURIComponent(code)}`)
  } catch (err) {
    next(err)
  }
}

export async function exchangeGoogleCode(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const { code } = req.body as { code?: string }
    if (!code || typeof code !== 'string') {
      throw new AppError('Missing Google authentication code', 400)
    }

    const consumed = await GoogleAuthCode.findOneAndUpdate(
      {
        code,
        usedAt: { $exists: false },
        expiresAt: { $gt: new Date() }
      },
      { $set: { usedAt: new Date() } },
      { new: true }
    )

    if (!consumed) {
      throw new UnauthorizedError('Invalid or expired Google authentication code')
    }

    const user = await User.findById(consumed.userId)
    if (!user) {
      throw new UnauthorizedError('User not found')
    }

    const token = authService.signToken(user._id.toString())
    success(res, { token, user }, 'Logged in successfully')
  } catch (err) {
    next(err)
  }
}
