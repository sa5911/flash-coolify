export const API_BASE_URL = (typeof process !== "undefined" ? process.env.NEXT_PUBLIC_API_BASE_URL : undefined) ?? "http://m8cgkg40400sg0kckw4804w4.46.202.194.55.sslip.io";

if (typeof window !== "undefined") {
  console.log("[Config] Frontend API Base URL:", API_BASE_URL);
}

/**
 * Get the full URL for a file/attachment.
 * Handles both B2 cloud URLs (https://...) and local URLs (/uploads/...).
 */
export function getFileUrl(url: string | null | undefined): string | null {
  if (!url) return null;
  // If it's already a full URL (B2 or external), return as-is
  if (url.startsWith("http://") || url.startsWith("https://")) {
    return url;
  }
  // Otherwise, prepend the API base URL
  return `${API_BASE_URL}${url.startsWith("/") ? url : `/${url}`}`;
}
