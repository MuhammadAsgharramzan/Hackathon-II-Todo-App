// API utility functions for the Todo App
// Using internal API routes for Vercel compatibility
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

interface ApiOptions {
  method?: string;
  headers?: HeadersInit;
  body?: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async request<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
    // For internal API routes, don't prepend baseUrl
    let url = endpoint.startsWith('/api/') ? endpoint : `${this.baseUrl}${endpoint}`;

    const defaultHeaders = {
      'Content-Type': 'application/json',
    };

    const token = localStorage.getItem('authToken');
    if (token) {
      defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    const config: RequestInit = {
      method: options.method || 'GET',
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
      body: options.body,
    };

    try {
      const response = await fetch(url, config);

      // Handle 401 Unauthorized - just remove token and throw error for caller to handle
      if (response.status === 401) {
        localStorage.removeItem('authToken');
        throw new Error('Unauthorized. Please log in again.');
      }

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`API request failed: ${response.status} - ${errorData}`);
      }

      // Handle successful responses
      if (response.status === 204) {
        // No content
        return {} as T;
      }

      return await response.json();
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  // Authentication methods
  async login(email: string, password: string) {
    // Call the internal API route that proxies to the backend
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const errorData = await response.text();
      throw new Error(errorData);
    }

    const data = await response.json();
    // Store the actual token from the backend response
    // The backend returns access_token field
    if (data.access_token) {
      localStorage.setItem('authToken', data.access_token);
    }
    return data;
  }

  async register(email: string, password: string) {
    // Call the internal API route that proxies to the backend
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const errorData = await response.text();
      throw new Error(errorData);
    }

    return await response.json();
  }

  // Task methods
  async getTasks(): Promise<any[]> {
    return this.request('/api/tasks');
  }

  async getTask(id: number): Promise<any> {
    return this.request(`/api/tasks/${id}`);
  }

  async createTask(taskData: any): Promise<any> {
    return this.request('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(id: number, taskData: any): Promise<any> {
    return this.request(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(id: number): Promise<void> {
    await this.request(`/api/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(id: number): Promise<any> {
    return this.request(`/api/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify({ toggleComplete: true }),
    });
  }

  // Chat methods
  async chat(message: string, conversationId?: number): Promise<any> {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message, conversation_id: conversationId }),
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);