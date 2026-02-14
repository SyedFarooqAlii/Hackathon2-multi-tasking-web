'use client';

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { getAuthToken } from '../lib/auth';

// Types for our chat functionality
type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
};

type ChatProps = {
  userId: string;
};

export default function ChatComponent({ userId }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const { user } = useAuth(); // Get the full user object to verify user ID
  const router = useRouter();

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get auth token from localStorage
      const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token') : null;

      // Call the backend chat API
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/chat/${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: conversationId || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if this is a new conversation
      if (data.conversation_id && !conversationId) {
        setConversationId(data.conversation_id);
        // Store conversation ID in localStorage for persistence
        localStorage.setItem('currentConversationId', data.conversation_id.toString());
      }

      // Add assistant message to UI
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to UI
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Load conversation from localStorage on component mount
  useEffect(() => {
    const savedConversationId = localStorage.getItem('currentConversationId');
    if (savedConversationId) {
      setConversationId(parseInt(savedConversationId, 10));
    }
  }, []);

  // Load conversation history if conversationId exists
  useEffect(() => {
    const loadConversationHistory = async () => {
      if (!conversationId || messages.length > 0) return; // Don't load if we already have messages

      try {
        setIsLoading(true);

        // For now, we don't have an endpoint to load conversation history
        // In a real implementation, you would call an API to load previous messages
        console.log('Loading conversation history for:', conversationId);
      } catch (error) {
        console.error('Error loading conversation history:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadConversationHistory();
  }, [conversationId]);

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Chat header */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 sm:px-6">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
              <span className="text-white text-sm font-medium">AI</span>
            </div>
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-900">Todo Assistant</p>
            <p className="text-xs text-gray-500">Manage your tasks with AI</p>
          </div>
        </div>
      </div>

      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Welcome to your AI Todo Assistant!</h3>
            <p className="text-gray-500 max-w-md">
              I can help you manage your tasks. Try saying "Add a task to buy groceries" or "Show my tasks".
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className={`text-xs mt-1 ${message.role === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 rounded-lg px-4 py-2 max-w-[80%]">
              <div className="flex space-x-2">
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></div>
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-75"></div>
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-gray-200 bg-white p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
            placeholder="Type your message here..."
            className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            aria-label="Type your message"
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="rounded-lg bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Send message"
          >
            Send
          </button>
        </form>
        <div className="mt-2 text-xs text-gray-500 text-center">
          {conversationId ? `Conversation ID: ${conversationId}` : 'New conversation'}
        </div>
      </div>
    </div>
  );
}