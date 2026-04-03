import Joi from 'joi'

export const updateProfileSchema = Joi.object({
  university: Joi.string().trim().max(200).optional().allow(''),
  programOfStudy: Joi.string().trim().max(200).optional().allow(''),
  primarySport: Joi.string().trim().max(100).optional().allow(''),
  yearOfStudy: Joi.string()
    .valid('Year 1', 'Year 2', 'Year 3', 'Year 4', 'Postgraduate', 'Professional', '')
    .optional(),
  avatarUrl: Joi.string().uri().optional().allow(''),
  bio: Joi.string().trim().max(500).optional().allow('')
})
