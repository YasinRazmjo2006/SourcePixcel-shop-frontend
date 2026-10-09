// lib/utils/validators.ts

// ─── Iranian Mobile Number ────────────────────────────────────────────────────

/**
 * Validate Iranian mobile number.
 * Format: 09XXXXXXXXX (11 digits, starts with 09)
 */
export function isValidIranianMobile(mobile: string): boolean {
  const cleaned = mobile.replace(/[\s\-()]/g, "");
  return /^09\d{9}$/.test(cleaned);
}

/**
 * Normalize Iranian mobile number (keep only digits).
 */
export function normalizeMobile(mobile: string): string {
  return mobile.replace(/[^0-9]/g, "");
}

/**
 * Format Iranian mobile for display: 0912 345 6789
 */
export function formatMobileDisplay(mobile: string): string {
  const cleaned = normalizeMobile(mobile);
  if (cleaned.length !== 11) return mobile;
  return `${cleaned.slice(0, 4)} ${cleaned.slice(4, 7)} ${cleaned.slice(7)}`;
}

// ─── Email ────────────────────────────────────────────────────────────────────

/**
 * Validate email address.
 */
export function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ─── National ID (Melli Code) ─────────────────────────────────────────────────

/**
 * Validate Iranian national ID (10 digits with checksum).
 */
export function isValidIranianNationalId(code: string): boolean {
  const cleaned = code.replace(/[^0-9]/g, "");
  if (cleaned.length !== 10) return false;
  if (/^(\d)\1{9}$/.test(cleaned)) return false;

  const check = parseInt(cleaned[9], 10);
  let sum = 0;
  for (let i = 0; i < 9; i++) {
    sum += parseInt(cleaned[i], 10) * (10 - i);
  }
  const remainder = sum % 11;
  return remainder < 2 ? check === remainder : check === 11 - remainder;
}

// ─── Postal Code ──────────────────────────────────────────────────────────────

/**
 * Validate Iranian postal code (10 digits).
 */
export function isValidIranianPostalCode(code: string): boolean {
  const cleaned = code.replace(/[^0-9]/g, "");
  return /^\d{10}$/.test(cleaned);
}

// ─── Password ─────────────────────────────────────────────────────────────────

/**
 * Check password strength.
 * Returns: 'weak' | 'medium' | 'strong'
 */
export function getPasswordStrength(password: string): "weak" | "medium" | "strong" {
  if (password.length < 6) return "weak";
  
  let score = 0;
  if (password.length >= 8) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^a-zA-Z0-9]/.test(password)) score++;
  
  if (score >= 4) return "strong";
  if (score >= 2) return "medium";
  return "weak";
}

/**
 * Validate password (minimum 6 characters).
 */
export function isValidPassword(password: string): boolean {
  return password.length >= 6;
}
