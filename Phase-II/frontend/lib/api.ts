// API utility functions for the Todo App

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

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
    const url = `${this.baseUrl}${endpoint}`;

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

      // Handle 401 Unauthorized
      if (response.status === 401) {
        localStorage.removeItem('authToken');
        window.location.href = '/login';
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
    // In a real app, this would be an API call to the backend
    // For now, we'll simulate a login and return a mock JWT token
    // The backend expects a JWT with a "sub" field containing the user ID
    const mockUserId = email.replace(/[^\w]/g, '_'); // Create a safe user ID from email
    const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
    const payload = btoa(JSON.stringify({
      sub: mockUserId,
      exp: Math.floor(Date.now() / 1000) + 3600, // 1 hour expiry
      iat: Math.floor(Date.now() / 1000) // issued at time
    }));
    const token = `${header}.${payload}.mock-signature`;

    localStorage.setItem('authToken', token);
    return { token };
  }

  async register(email: string, password: string) {
    // In a real app, this would be an API call to the backend
    // For now, we'll simulate registration
    return { success: true };
  }

  // Task methods
  async getTasks(): Promise<any[]> {
    return this.request('/tasks');
  }

  async getTask(id: number): Promise<any> {
    return this.request(`/tasks/${id}`);
  }

  async createTask(taskData: any): Promise<any> {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(id: number, taskData: any): Promise<any> {
    return this.request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(id: number): Promise<void> {
    await this.request(`/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(id: number): Promise<any> {
    return this.request(`/tasks/${id}/toggle-complete`, {
      method: 'PATCH',
    });
  }

  // Chat methods
  async chat(message: string, conversationId?: number): Promise<any> {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message, conversation_id: conversationId }),
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);