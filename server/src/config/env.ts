import 'dotenv/config'
import Joi from 'joi'

const schema = Joi.object({
  // Default matches SERVER_URL default so OAuth callbacks stay consistent when .env is absent
  PORT: Joi.number().default(7000),
  NODE_ENV: Joi.string().valid('development', 'production', 'test').default('development'),
  MONGODB_URI: Joi.string().required(),
  JWT_SECRET: Joi.string().min(16).required(),
  JWT_EXPIRES_IN: Joi.string().default('7d'),
  CORS_ORIGIN: Joi.string().default('http://localhost:5173'),
  ALLOWED_ORIGINS: Joi.string().default('http://localhost:5173'),
  ML_SERVICE_URL: Joi.string().default('http://localhost:8001'),
  GOOGLE_SHEETS_CREDENTIALS_PATH: Joi.string().optional(),
  GOOGLE_SHEETS_CREDENTIALS_JSON: Joi.string().optional(),
  GOOGLE_SHEETS_SPREADSHEET_ID: Joi.string().optional(),
  GOOGLE_SHEETS_WORKSHEET_NAME: Joi.string().optional(),
  GOOGLE_CLIENT_ID: Joi.string().optional(),
  GOOGLE_CLIENT_SECRET: Joi.string().optional(),
  BETTER_AUTH_SECRET: Joi.string().min(16).optional(),
  SERVER_URL: Joi.string().default('http://localhost:7000'),
  CLIENT_URL: Joi.string().default('http://localhost:5173'),
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
  // NOTE: corsOrigin is exported for reference but the CORS middleware in app.ts only
  // reads allowedOrigins (ALLOWED_ORIGINS). Update ALLOWED_ORIGINS to control CORS.
  corsOrigin: value.CORS_ORIGIN as string,
  allowedOrigins: (value.ALLOWED_ORIGINS as string).split(',').map((s: string) => s.trim()),
  mlServiceUrl: value.ML_SERVICE_URL as string,
  googleSheetsCredentialsPath: value.GOOGLE_SHEETS_CREDENTIALS_PATH as string | undefined,
  googleSheetsCredentialsJson: value.GOOGLE_SHEETS_CREDENTIALS_JSON as string | undefined,
  googleSheetsSpreadsheetId: value.GOOGLE_SHEETS_SPREADSHEET_ID as string | undefined,
  googleSheetsWorksheetName: value.GOOGLE_SHEETS_WORKSHEET_NAME as string | undefined,
  googleClientId: value.GOOGLE_CLIENT_ID as string | undefined,
  googleClientSecret: value.GOOGLE_CLIENT_SECRET as string | undefined,
  betterAuthSecret: (value.BETTER_AUTH_SECRET as string | undefined) ?? (value.JWT_SECRET as string),
  serverUrl: value.SERVER_URL as string,
  clientUrl: value.CLIENT_URL as string,
  logLevel: value.LOG_LEVEL as string,
  isDev: value.NODE_ENV === 'development'
}
