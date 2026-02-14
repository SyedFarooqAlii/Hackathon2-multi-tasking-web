// Frontend API client for the secure todo application
// Handles JWT token management and API communication

import axios from 'axios'
import { Todo, TodoCreate, TodoUpdate, User, AuthResponse } from './types'

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'

// Create axios instance with defaults
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add JWT token
apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle 401 errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Remove token and redirect to login
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token')
        sessionStorage.removeItem('auth_token')
      }
      // In a real app, you'd want to redirect to login page
      // window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API client class
class ApiClient {
  // Authentication endpoints
  async register(email: string, password: string): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/users/register', {
      email,
      password,
    })
    // Save token after successful registration
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token)
    }
    return response.data
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/users/login', {
      email,
      password,
    })
    // Save token after successful login
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token)
    }
    return response.data
  }

  async logout(): Promise<void> {
    // Remove token from storage
    localStorage.removeItem('auth_token')
    sessionStorage.removeItem('auth_token')
  }

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/users/me')
    return response.data
  }

  // Helper function to get user ID from JWT token
  private getUserIdFromToken(): string | null {
    const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
    if (!token) {
      return null;
    }

    try {
      // Decode JWT token (split by '.' and decode the payload part)
      const parts = token.split('.');
      if (parts.length !== 3) {
        console.error('Invalid JWT token format');
        return null;
      }

      // Decode the payload (second part)
      const payload = parts[1];
      // Add padding if needed
      const paddedPayload = payload + '='.repeat((4 - payload.length % 4) % 4);
      const decodedPayload = atob(paddedPayload);
      const parsedPayload = JSON.parse(decodedPayload);

      return parsedPayload.sub; // 'sub' is the subject claim containing the user ID
    } catch (error) {
      console.error('Error decoding JWT token:', error);
      return null;
    }
  }

  // Todo endpoints - use /users/me/ endpoints as the backend handles user identification from JWT
  async getTodos(): Promise<{ tasks: Todo[] }> {
    try {
      console.log('Making GET request to /users/me/tasks');
      const response = await apiClient.get<{ tasks: Todo[] }>('/users/me/tasks');
      console.log('GET response:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error getting todos:', error);
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
      throw error;
    }
  }

  async createTodo(todoData: TodoCreate): Promise<Todo> {
    try {
      console.log('Making POST request to /users/me/tasks with data:', todoData);
      const response = await apiClient.post<Todo>('/users/me/tasks', todoData);
      console.log('POST response:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error creating todo:', error);
      console.error('Error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        config: error.config ? {
          method: error.config.method,
          url: error.config.url,
          data: error.config.data,
          headers: error.config.headers
        } : null
      });
      throw error;
    }
  }

  async getTodoById(todoId: string): Promise<Todo> {
    try {
      const response = await apiClient.get<Todo>(`/users/me/tasks/${todoId}`);
      return response.data;
    } catch (error: any) {
      console.error('Error getting todo by ID:', error);
      throw error;
    }
  }

  async updateTodo(todoId: string, todoData: TodoUpdate): Promise<Todo> {
    try {
      const response = await apiClient.put<Todo>(`/users/me/tasks/${todoId}`, todoData);
      return response.data;
    } catch (error: any) {
      console.error('Error updating todo:', error);
      throw error;
    }
  }

  async deleteTodo(todoId: string): Promise<void> {
    try {
      await apiClient.delete(`/users/me/tasks/${todoId}`);
    } catch (error: any) {
      console.error('Error deleting todo:', error);
      throw error;
    }
  }

  async toggleTodoCompletion(todoId: string, completed: boolean): Promise<Todo> {
    try {
      const response = await apiClient.patch<Todo>(`/users/me/tasks/${todoId}/complete`, {
        completed,
      });
      return response.data;
    } catch (error: any) {
      console.error('Error toggling todo completion:', error);
      throw error;
    }
  }
}

// Create a singleton instance of the API client
export const apiClientInstance = new ApiClient()

// Export convenience functions
export const todoApi = {
  getTodos: () => apiClientInstance.getTodos(),
  createTodo: (data: TodoCreate) => apiClientInstance.createTodo(data),
  getTodoById: (id: string) => apiClientInstance.getTodoById(id),
  updateTodo: (id: string, data: TodoUpdate) => apiClientInstance.updateTodo(id, data),
  deleteTodo: (id: string) => apiClientInstance.deleteTodo(id),
  toggleTodoCompletion: (id: string, completed: boolean) =>
    apiClientInstance.toggleTodoCompletion(id, completed),
}

export const authApi = {
  register: (email: string, password: string) => apiClientInstance.register(email, password),
  login: (email: string, password: string) => apiClientInstance.login(email, password),
  logout: () => apiClientInstance.logout(),
  getCurrentUser: () => apiClientInstance.getCurrentUser(),
}