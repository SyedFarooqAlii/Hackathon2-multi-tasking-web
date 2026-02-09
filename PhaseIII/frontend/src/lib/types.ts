// Type definitions for the Todo application

export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
  category: string;
  due_date?: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  completed?: boolean;
  category: string;
  due_date?: string;
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  category?: string;
  due_date?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  success: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
}