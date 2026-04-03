import Joi from 'joi'

export const updateUserSchema = Joi.object({
  name: Joi.string().trim().min(2).max(100).required()
})
