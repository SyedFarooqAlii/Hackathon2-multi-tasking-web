/**
 * Service for handling chat-related API calls
 */

import axios from 'axios';

interface ChatRequest {
  message: string;
  conversation_id?: number;
}

interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<{
    name: string;
    arguments: Record<string, any>;
  }>;
}

class ChatService {
  private baseUrl: string;
  private token: string | null;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL || '';
    this.token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  }

  /**
   * Send a message to the chat API
   */
  async sendMessage(userId: string, message: string, conversationId?: number): Promise<ChatResponse> {
    try {
      const response = await axios.post<ChatResponse>(
        `${this.baseUrl}/api/${userId}/chat`,
        {
          message,
          conversation_id: conversationId
        } as ChatRequest,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`
          }
        }
      );

      return response.data;
    } catch (error: any) {
      console.error('Error sending message:', error);
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        console.error('Response headers:', error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.error('Request:', error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.error('Error message:', error.message);
      }
      throw error;
    }
  }

  /**
   * Get conversation history
   */
  async getConversationHistory(userId: string, conversationId: number): Promise<any[]> {
    try {
      // Note: This is a placeholder as we don't have a specific endpoint for retrieving conversation history
      // In a real implementation, you would have an endpoint like:
      // return (await axios.get(`${this.baseUrl}/api/${userId}/conversations/${conversationId}/messages`)).data;
      return [];
    } catch (error) {
      console.error('Error getting conversation history:', error);
      throw error;
    }
  }

  /**
   * Create a new conversation
   */
  async createConversation(userId: string): Promise<{ conversation_id: number }> {
    try {
      // For now, a new conversation is initiated when sending the first message without a conversation_id
      // This method is included for future extensibility
      return { conversation_id: Date.now() }; // Placeholder
    } catch (error) {
      console.error('Error creating conversation:', error);
      throw error;
    }
  }
}

export const chatService = new ChatService();
export type { ChatRequest, ChatResponse };