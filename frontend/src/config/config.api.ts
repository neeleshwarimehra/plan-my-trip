const rawBaseUrl = import.meta.env.VITE_API_BASE_URL || "";

// Remove any trailing slash; if empty in production, falls back to same-origin /api proxy
export const API_BASE_URL = rawBaseUrl.replace(/\/+$/, "");

export const API_ENDPOINTS = {
  health: `${API_BASE_URL}/api/health`,
  planTrip: `${API_BASE_URL}/api/trips/plan`,
  trips: `${API_BASE_URL}/api/trips`,
  tripById: (id: string) => `${API_BASE_URL}/api/trips/${id}`,
} as const;