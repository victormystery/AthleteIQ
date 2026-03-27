export const isEmail = (val: string): boolean =>
  /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/.test(val)

export const minLength = (min: number) => (val: string): boolean =>
  typeof val === 'string' && val.length >= min

export const required = (val: unknown): boolean =>
  val !== null && val !== undefined && val !== ''

export const isLettersOnly = (val: string): boolean =>
  /^[A-Za-z\s]+$/.test(val)

export const isStrongPassword = (val: string): boolean =>
  val.length >= 8 &&
  /[A-Z]/.test(val) &&
  /[0-9]/.test(val) &&
  /[^A-Za-z0-9]/.test(val)
