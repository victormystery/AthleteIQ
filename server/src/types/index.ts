import type { Request } from 'express'
import type { IUser } from '../models/User.model.js'

export interface AuthenticatedRequest extends Request {
  user: IUser
}
