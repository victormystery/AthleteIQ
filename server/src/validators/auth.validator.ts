import Joi from 'joi'

export const registerSchema = Joi.object({
  name: Joi.string().pattern(/^[A-Za-z\s]+$/).min(2).max(100).required()
    .messages({ 'string.pattern.base': 'Name must contain letters only (no numbers or special characters)' }),
  email: Joi.string().email().required(),
  password: Joi.string().min(8).max(128)
    .pattern(/[A-Z]/)
    .pattern(/[0-9]/)
    .pattern(/[^A-Za-z0-9]/)
    .required()
    .messages({
      'string.pattern.base': 'Password must include an uppercase letter, a number, and a special character'
    })
})

export const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().required()
})
