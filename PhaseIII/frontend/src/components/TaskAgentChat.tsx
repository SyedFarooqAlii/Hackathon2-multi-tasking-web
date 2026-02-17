'use client';

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { todoApi } from '../lib/api';

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
};

type TaskAgentChatProps = {
  onTaskUpdate?: () => void; // Callback to refresh tasks after agent actions
};

export default function TaskAgentChat({ onTaskUpdate }: TaskAgentChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { user } = useAuth();

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Intent detection function
  const detectIntent = (message: string): { intent: string; params: any } => {
    const lowerMessage = message.toLowerCase().trim();

    // Add task
    if (lowerMessage.match(/^(add|create|new)\s+(task|todo)\s+(.+)/i)) {
      const match = lowerMessage.match(/^(add|create|new)\s+(task|todo)\s+(.+)/i);
      return { intent: 'add_task', params: { title: match![3] } };
    }

    // Delete task
    if (lowerMessage.match(/^(delete|remove)\s+(task|todo)\s+(\d+)/i)) {
      const match = lowerMessage.match(/^(delete|remove)\s+(task|todo)\s+(\d+)/i);
      return { intent: 'delete_task', params: { taskNumber: parseInt(match![3]) } };
    }

    // Complete task
    if (lowerMessage.match(/^(complete|finish|done)\s+(task|todo)\s+(\d+)/i)) {
      const match = lowerMessage.match(/^(complete|finish|done)\s+(task|todo)\s+(\d+)/i);
      return { intent: 'complete_task', params: { taskNumber: parseInt(match![3]) } };
    }

    // Show tasks
    if (lowerMessage.match(/^(show|list|get|view)\s+(my\s+)?(tasks|todos)/i)) {
      return { intent: 'show_tasks', params: {} };
    }

    // Unknown intent
    return { intent: 'unknown', params: {} };
  };

  // Execute task actions
  const executeTaskAction = async (intent: string, params: any): Promise<string> => {
    try {
      switch (intent) {
        case 'add_task': {
          await todoApi.createTodo({
            title: params.title,
            description: '',
            completed: false,
            category: 'general'
          });
          if (onTaskUpdate) onTaskUpdate();
          return `✅ Task created: "${params.title}"`;
        }

        case 'delete_task': {
          // Get all tasks to find the task by number
          const { tasks } = await todoApi.getTodos();

          if (params.taskNumber < 1 || params.taskNumber > tasks.length) {
            return `❌ Task #${params.taskNumber} not found. You have ${tasks.length} tasks.`;
          }

          const taskToDelete = tasks[params.taskNumber - 1];
          await todoApi.deleteTodo(taskToDelete.id);
          if (onTaskUpdate) onTaskUpdate();
          return `✅ Task #${params.taskNumber} deleted: "${taskToDelete.title}"`;
        }

        case 'complete_task': {
          // Get all tasks to find the task by number
          const { tasks } = await todoApi.getTodos();

          if (params.taskNumber < 1 || params.taskNumber > tasks.length) {
            return `❌ Task #${params.taskNumber} not found. You have ${tasks.length} tasks.`;
          }

          const taskToComplete = tasks[params.taskNumber - 1];
          await todoApi.toggleTodoCompletion(taskToComplete.id, true);
          if (onTaskUpdate) onTaskUpdate();
          return `✅ Task #${params.taskNumber} completed: "${taskToComplete.title}"`;
        }

        case 'show_tasks': {
          const { tasks } = await todoApi.getTodos();

          if (tasks.length === 0) {
            return '📝 You have no tasks yet. Try: "add task buy milk"';
          }

          let taskList = `📝 You have ${tasks.length} task(s):\n\n`;
          tasks.forEach((task: any, index: number) => {
            const status = task.completed ? '✅' : '⬜';
            taskList += `${status} ${index + 1}. ${task.title}\n`;
          });
          return taskList;
        }

        default:
          return '❓ I didn\'t understand that. Try:\n• "add task [description]"\n• "delete task [number]"\n• "complete task [number]"\n• "show my tasks"';
      }
    } catch (error: any) {
      console.error('Task action error:', error);
      if (error.response?.status === 401) {
        return '🔒 Authentication error. Please log in again.';
      }
      return `❌ Error: ${error.response?.data?.detail || error.message || 'Something went wrong'}`;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      // Detect intent
      const { intent, params } = detectIntent(currentInput);

      // Execute action
      const responseText = await executeTaskAction(intent, params);

      // Add assistant response
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: responseText,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error processing message:', error);

      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: '❌ Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 border border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          🤖 AI Task Agent
        </h3>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          Natural language commands
        </span>
      </div>

      {/* Messages */}
      <div className="h-64 overflow-y-auto mb-4 space-y-3 bg-gray-50 dark:bg-gray-900 rounded-lg p-3">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 dark:text-gray-400 text-sm py-8">
            <p className="mb-2">👋 Hi! I'm your AI task agent.</p>
            <p className="text-xs">Try: "add task buy groceries"</p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 dark:bg-gray-700 rounded-lg px-4 py-2">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type a command... (e.g., add task buy milk)"
          className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white text-sm"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm font-medium"
        >
          Send
        </button>
      </form>

      {/* Help text */}
      <div className="mt-3 text-xs text-gray-500 dark:text-gray-400">
        <p className="font-semibold mb-1">Commands:</p>
        <ul className="space-y-1 ml-2">
          <li>• add task [description]</li>
          <li>• delete task [number]</li>
          <li>• complete task [number]</li>
          <li>• show my tasks</li>
        </ul>
      </div>
    </div>
  );
}
