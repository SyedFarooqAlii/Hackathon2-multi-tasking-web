// Authentication management for the todo application
// Handles token management and authentication state

import { User, AuthResponse } from './types'
import { apiClientInstance } from './api'

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')
    return !!token
  }
  return false
}

// Get current user info from token or API
export const getCurrentUser = async (): Promise<User | null> => {
  if (!isAuthenticated()) {
    return null
  }

  try {
    const user = await apiClientInstance.getCurrentUser()
    return user
  } catch (error) {
    console.error('Error getting current user:', error)
    // If API call fails, we might still have a valid token
    // Return null to indicate need for re-authentication
    return null
  }
}

// Register a new user
export const registerUser = async (
  email: string,
  password: string
): Promise<AuthResponse> => {
  try {
    const response = await apiClientInstance.register(email, password)
    return response
  } catch (error) {
    console.error('Registration error:', error)
    throw error
  }
}

// Login a user
export const loginUser = async (
  email: string,
  password: string
): Promise<AuthResponse> => {
  try {
    const response = await apiClientInstance.login(email, password)
    return response
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}

// Logout user
export const logoutUser = async (): Promise<void> => {
  try {
    await apiClientInstance.logout()
  } catch (error) {
    console.error('Logout error:', error)
    // Even if logout API call fails, we should clear local token
  }
  // Clear local storage
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token')
    sessionStorage.removeItem('auth_token')
  }
}

// Get auth token
export const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')
  }
  return null
}

// Set auth token
export const setAuthToken = (token: string, remember: boolean = true): void => {
  if (typeof window !== 'undefined') {
    if (remember) {
      localStorage.setItem('auth_token', token)
    } else {
      sessionStorage.setItem('auth_token', token)
    }
  }
}