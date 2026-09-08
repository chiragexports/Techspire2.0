const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== 'undefined' && window.location.hostname.includes('vercel.app')
    ? '/api/backend'
    : 'http://127.0.0.1:8000/api');

class ApiClient {
  private getAccessToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('techspire_access_token');
  }

  private getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('techspire_refresh_token');
  }

  private setTokens(access: string, refresh?: string) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('techspire_access_token', access);
    if (refresh) localStorage.setItem('techspire_refresh_token', refresh);
  }

  public clearTokens() {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('techspire_access_token');
    localStorage.removeItem('techspire_refresh_token');
    localStorage.removeItem('techspire_user');
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string> || {}),
    };

    const token = this.getAccessToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    let response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle token expiration & attempt refresh
    if (response.status === 401 && this.getRefreshToken() && !endpoint.includes('auth/refresh') && !endpoint.includes('auth/login')) {
      const refreshed = await this.refreshAccessToken();
      if (refreshed) {
        headers['Authorization'] = `Bearer ${this.getAccessToken()}`;
        response = await fetch(url, {
          ...options,
          headers,
        });
      }
    }

    if (!response.ok) {
      let errorMessage = `Server error (${response.status})`;
      try {
        const errorData = await response.json();
        if (errorData.error) {
          errorMessage = typeof errorData.error === 'string' ? errorData.error : JSON.stringify(errorData.error);
        } else if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (errorData.message) {
          errorMessage = errorData.message;
        } else if (typeof errorData === 'object' && errorData !== null) {
          const keys = Object.keys(errorData);
          if (keys.length > 0) {
            const firstKey = keys[0];
            const val = errorData[firstKey];
            const cleanVal = Array.isArray(val) ? val[0] : String(val);
            if (firstKey === 'non_field_errors' || firstKey === 'detail') {
              errorMessage = cleanVal;
            } else {
              const formattedKey = firstKey.charAt(0).toUpperCase() + firstKey.slice(1).replace(/_/g, ' ');
              errorMessage = `${formattedKey}: ${cleanVal}`;
            }
          }
        }
      } catch {
        if (response.status === 500) {
          errorMessage = 'Server is currently processing your request. Please check your credentials or try again.';
        } else if (response.status === 404) {
          errorMessage = 'The requested resource was not found.';
        } else if (response.status === 403) {
          errorMessage = 'Access forbidden. Please sign in with appropriate permissions.';
        } else if (response.status === 401) {
          errorMessage = 'Invalid email or password.';
        }
      }
      throw new Error(errorMessage);
    }

    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  private async refreshAccessToken(): Promise<boolean> {
    const refresh = this.getRefreshToken();
    if (!refresh) return false;

    try {
      const res = await fetch(`${API_BASE_URL}/auth/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
      });

      if (res.ok) {
        const data = await res.json();
        this.setTokens(data.access, data.refresh);
        return true;
      }
      this.clearTokens();
      return false;
    } catch {
      this.clearTokens();
      return false;
    }
  }

  // HTTP Helper Methods
  get<T>(endpoint: string, headers?: Record<string, string>): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET', headers });
  }

  post<T>(endpoint: string, data?: unknown, headers?: Record<string, string>): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
      headers,
    });
  }

  put<T>(endpoint: string, data?: unknown, headers?: Record<string, string>): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
      headers,
    });
  }

  patch<T>(endpoint: string, data?: unknown, headers?: Record<string, string>): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
      headers,
    });
  }

  delete<T>(endpoint: string, headers?: Record<string, string>): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE', headers });
  }
}

export const api = new ApiClient();
