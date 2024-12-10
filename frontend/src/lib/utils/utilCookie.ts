// Function to set a cookie (only in the browser)
export function setCookie(name: string, value: string, days: number = 7): void {
  if (typeof window !== 'undefined') {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000); // Default expiry of 7 days
    const expiresString = `expires=${expires.toUTCString()}`;
    document.cookie = `${name}=${value}; ${expiresString}; path=/`;
  }
}

// Function to get a cookie by name (only in the browser)
export function getCookie(name: string): string | null {
  if (typeof window !== 'undefined') {
    const nameEQ = `${name}=`;
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === ' ') {
        c = c.substring(1, c.length); // Trim leading spaces
      }
      if (c.indexOf(nameEQ) === 0) {
        return c.substring(nameEQ.length, c.length); // Return the cookie value
      }
    }
  }
  return null; // Return null if not found
}

// Function to erase a cookie by name (only in the browser)
export function eraseCookie(name: string): void {
  if (typeof window !== 'undefined') {
    document.cookie = `${name}=; Max-Age=-99999999; path=/`;
  }
}
