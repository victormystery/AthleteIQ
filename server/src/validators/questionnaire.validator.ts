import Joi from 'joi'

export const questionnaireSchema = Joi.object({
  academic_level: Joi.string()
    .valid('Year 1', 'Year 2', 'Year 3', 'Year 4', 'Postgraduate')
    .required()
    .messages({ 'any.required': 'Academic level is required' }),

  primary_sport: Joi.string().trim().min(2).max(100).required()
    .messages({ 'any.required': 'Primary sport is required' }),

  participation_years: Joi.string()
    .valid('Less than 1 year', '1-2 years', '3-5 years', 'More than 5 years')
    .required()
    .messages({ 'any.required': 'Participation years is required' }),

  participation_level: Joi.string()
    .valid('Not active', 'Recreational', 'University/School team', 'Club or academy', 'Elite/competitive pathway')
    .required()
    .messages({ 'any.required': 'Participation level is required' }),

  fitness_level: Joi.number().integer().min(1).max(5).required()
    .messages({ 'any.required': 'Fitness level is required' }),

  technical_skill: Joi.number().integer().min(1).max(5).required()
    .messages({ 'any.required': 'Technical skill is required' }),

  leadership: Joi.number().integer().min(1).max(5).required()
    .messages({ 'any.required': 'Leadership rating is required' }),

  data_comfort: Joi.number().integer().min(1).max(5).required()
    .messages({ 'any.required': 'Data comfort rating is required' }),

  motivation: Joi.string()
    .valid('Competition and performance', 'Health and fitness', 'Helping or coaching others', 'Academic or career opportunity', 'Fame, media, or recognition')
    .required()
    .messages({ 'any.required': 'Motivation is required' }),

  career_importance: Joi.string()
    .valid(
      'Not important',
      'Slightly important',
      'Moderately important',
      'Very important',
      'My main career focus'
    )
    .required()
    .messages({ 'any.required': 'Career importance is required' }),

  work_environment: Joi.string()
    .valid('On-field / practical', 'Office / management', 'Laboratory / science / clinical', 'Media / creative', 'A mix of environments')
    .required()
    .messages({ 'any.required': 'Work environment is required' }),

  education_training_level: Joi.string()
    .valid(
      'Short courses or certifications only',
      'Diploma',
      "Bachelor's degree or add-on program",
      "Master's degree",
      'Medical/clinical or doctoral pathway'
    )
    .required()
    .messages({ 'any.required': 'Education/training level is required' }),

  biggest_challenge: Joi.string()
    .valid(
      'Academic workload',
      'Time management',
      'Financial constraints',
      'Injury risk or health',
      'Lack of facilities or coaching',
      'Motivation'
    )
    .required()
    .messages({ 'any.required': 'Biggest challenge is required' }),

  injury_history: Joi.string()
    .valid('None', 'Minor (short recovery)', 'Moderate (missed competitions)', 'Severe (long-term impact)')
    .required()
    .messages({ 'any.required': 'Injury history is required' }),

  career_interests: Joi.array()
    .items(Joi.string().trim())
    .min(1)
    .max(3)
    .required()
    .messages({
      'any.required': 'Career interests are required',
      'array.min': 'Select at least 1 career interest',
      'array.max': 'Select at most 3 career interests'
    })
})
