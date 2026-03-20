import jwt from 'jsonwebtoken'
import { env } from '../config/env.js'
import { User } from '../models/index.js'
import type { IUser } from '../models/User.model.js'
import { AppError, UnauthorizedError } from '../utils/errors.js'

interface AuthResult {
  token: string
  user: IUser
}

interface RegisterResult {
  user: IUser
}

function signToken(userId: string): string {
  return jwt.sign({ sub: userId }, env.jwtSecret, {
    expiresIn: env.jwtExpiresIn as jwt.SignOptions['expiresIn']
  })
}

export async function register(name: string, email: string, password: string): Promise<RegisterResult> {
  const existing = await User.findOne({ email })
  if (existing) throw new AppError('Email already in use', 409)

  const user = await User.create({ name, email, password })
  return { user }
}

export async function login(email: string, password: string): Promise<AuthResult> {
  const user = await User.findOne({ email }).select('+password')
  if (!user || !(await user.comparePassword(password))) {
    throw new UnauthorizedError('Invalid email or password')
  }
  const token = signToken(user._id.toString())
  // password is excluded by toJSON() on the User model
  return { token, user }
}
