import type { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'
import { env } from '../config/env.js'
import { UnauthorizedError } from '../utils/errors.js'
import { User } from '../models/index.js'
import type { IUser } from '../models/User.model.js'

interface JwtPayload {
  sub: string
}

// Make Express.User resolve to IUser so all auth middleware
// shares the same type for req.user across the application.
declare global {
  namespace Express {
    interface Request {
      user?: IUser
    }

    interface User extends IUser {}
  }
}

export async function authenticate(
  req: Request,
  _res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const authHeader = req.headers.authorization
    if (!authHeader?.startsWith('Bearer ')) {
      throw new UnauthorizedError('No token provided')
    }
    const token = authHeader.split(' ')[1]
    const decoded = jwt.verify(token, env.jwtSecret) as JwtPayload
    const user = await User.findById(decoded.sub)
    if (!user) throw new UnauthorizedError('User not found')
    if (user.suspended) throw new UnauthorizedError('Account suspended')
    req.user = user
    next()
  } catch (err) {
    const error = err as Error
    if (error.name === 'JsonWebTokenError' || error.name === 'TokenExpiredError') {
      return next(new UnauthorizedError('Invalid or expired token'))
    }
    next(err)
  }
}
