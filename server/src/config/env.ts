import 'dotenv/config'
import Joi from 'joi'

const schema = Joi.object({
  PORT: Joi.number().default(3000),
  NODE_ENV: Joi.string().valid('development', 'production', 'test').default('development'),
  MONGODB_URI: Joi.string().required(),
  JWT_SECRET: Joi.string().min(16).required(),
  JWT_EXPIRES_IN: Joi.string().default('7d'),
  CORS_ORIGIN: Joi.string().default('http://localhost:5173'),
  ALLOWED_ORIGINS: Joi.string().default('http://localhost:5173'),
  ML_SERVICE_URL: Joi.string().default('http://localhost:8001'),
  GOOGLE_SHEETS_CREDENTIALS_PATH: Joi.string().optional(),
  GOOGLE_SHEETS_SPREADSHEET_ID: Joi.string().optional(),
  LOG_LEVEL: Joi.string().valid('error', 'warn', 'info', 'debug').default('info')
}).unknown(true)

const { error, value } = schema.validate(process.env)

if (error) {
  throw new Error(`Config validation error: ${error.message}`)
}

export const env = {
  port: value.PORT as number,
  nodeEnv: value.NODE_ENV as string,
  mongoUri: value.MONGODB_URI as string,
  jwtSecret: value.JWT_SECRET as string,
  jwtExpiresIn: value.JWT_EXPIRES_IN as string,
  corsOrigin: value.CORS_ORIGIN as string,
  allowedOrigins: (value.ALLOWED_ORIGINS as string).split(',').map((s: string) => s.trim()),
  mlServiceUrl: value.ML_SERVICE_URL as string,
  googleSheetsCredentialsPath: value.GOOGLE_SHEETS_CREDENTIALS_PATH as string | undefined,
  googleSheetsSpreadsheetId: value.GOOGLE_SHEETS_SPREADSHEET_ID as string | undefined,
  logLevel: value.LOG_LEVEL as string,
  isDev: value.NODE_ENV === 'development'
}
