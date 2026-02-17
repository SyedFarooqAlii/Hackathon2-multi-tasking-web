'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { Todo } from '../../lib/types';
import TaskAgentChat from '../../components/TaskAgentChat';

const TodosPage = () => {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState<Todo[]>([]);
  const [loadingTasks, setLoadingTasks] = useState(true);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    category: '',
    due_date: ''
  });
  const [editingTask, setEditingTask] = useState<Todo | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showCategorySuggestions, setShowCategorySuggestions] = useState(false);

  useEffect(() => {
    if (!loading && !user) {
      router.push('/auth/login');
    } else if (user) {
      fetchTasks();
    }
  }, [user, loading, router]);

  const fetchTasks = async () => {
    try {
      setLoadingTasks(true);

      // Fetch tasks from the backend API using the proper API client
      const { tasks } = await import('../../lib/api').then(mod => mod.todoApi.getTodos());

      // Ensure all tasks have the required new fields with defaults
      const tasksWithDefaults = tasks.map(task => ({
        ...task,
        category: task.category || '',
        due_date: task.due_date || undefined
      }));

      setTasks(tasksWithDefaults);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoadingTasks(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      if (editingTask) {
        // Update existing task via API
        await import('../../lib/api').then(mod =>
          mod.todoApi.updateTodo(editingTask.id, {
            title: newTask.title,
            description: newTask.description,
            category: newTask.category,
            due_date: newTask.due_date || undefined,
          })
        );
      } else {
        // Create new task via API
        await import('../../lib/api').then(mod =>
          mod.todoApi.createTodo({
            title: newTask.title,
            description: newTask.description,
            completed: false,
            category: newTask.category,
            due_date: newTask.due_date || undefined,
          })
        );
      }

      // Refresh the tasks list
      await fetchTasks();
      setNewTask({ title: '', description: '', category: '', due_date: '' });
      setShowCreateForm(false);
      setEditingTask(null);
    } catch (error) {
      console.error('Error saving task:', error);
    }
  };

  const handleEdit = (task: Todo) => {
    setEditingTask(task);
    setNewTask({
      title: task.title,
      description: task.description || '',
      category: task.category || '',
      due_date: task.due_date || ''
    });
    setShowCreateForm(true);
  };

  const handleDelete = async (id: string) => {
    try {
      // Delete task via API
      await import('../../lib/api').then(mod => mod.todoApi.deleteTodo(id));

      // Refresh the tasks list
      await fetchTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const toggleComplete = async (id: string) => {
    // Find the task in the current state
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    try {
      // Toggle task completion via API
      await import('../../lib/api').then(mod =>
        mod.todoApi.toggleTodoCompletion(id, !task.completed)
      );

      // Refresh the tasks list
      await fetchTasks();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <div className="animate-fade-in-up">
        {/* Page Header */}
        <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">My Tasks</h1>
                <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                  Manage your tasks efficiently
                </p>
              </div>
              <button
                onClick={() => {
                  setEditingTask(null);
                  setNewTask({ title: '', description: '', category: '', due_date: '' });
                  setShowCreateForm(!showCreateForm);
                }}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-all duration-200 flex items-center space-x-2 shadow-sm hover:shadow-md"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span>{showCreateForm ? 'Cancel' : 'Add Task'}</span>
              </button>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Create/Edit Task Form - Enhanced with Priority, Category, and Due Date */}
          {showCreateForm && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 mb-8 hover:shadow-xl transition-all duration-300 group">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-blue-600 dark:text-blue-400 group-hover:scale-110 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                {editingTask ? 'Edit Task' : 'Create New Task'}
              </h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Task Title *
                  </label>
                  <input
                    type="text"
                    id="title"
                    value={newTask.title}
                    onChange={(e) => setNewTask({...newTask, title: e.target.value})}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-all duration-200 shadow-sm focus:shadow-md hover:shadow-sm"
                    placeholder="Enter task title"
                    required
                    autoFocus
                  />
                </div>

                <div>
                  <label htmlFor="category" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Category
                  </label>
                  <div className="relative">
                    <input
                      type="text"
                      id="category"
                      value={newTask.category}
                      onChange={(e) => setNewTask({...newTask, category: e.target.value})}
                      onFocus={() => setShowCategorySuggestions(true)}
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-all duration-200 shadow-sm focus:shadow-md hover:shadow-sm"
                      placeholder="Work, Home, Gym, Personal, etc."
                    />

                    {showCategorySuggestions && (
                      <div className="absolute z-10 mt-1 w-full bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg max-h-40 overflow-y-auto">
                        {['Work', 'Home', 'Gym', 'Personal', 'Shopping', 'Health', 'Finance', 'Learning', 'Project', 'Other'].map((suggestion) => (
                          <button
                            key={suggestion}
                            type="button"
                            onClick={() => {
                              setNewTask({...newTask, category: suggestion});
                              setShowCategorySuggestions(false);
                            }}
                            className="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors duration-150 first:rounded-t-lg last:rounded-b-lg"
                          >
                            {suggestion}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>


                <div>
                  <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Due Date (Optional)
                  </label>
                  <input
                    type="date"
                    id="due_date"
                    value={newTask.due_date}
                    onChange={(e) => setNewTask({...newTask, due_date: e.target.value})}
                    min={new Date().toISOString().split('T')[0]}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-all duration-200 shadow-sm focus:shadow-md hover:shadow-sm"
                  />
                </div>

                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Description
                  </label>
                  <textarea
                    id="description"
                    value={newTask.description}
                    onChange={(e) => setNewTask({...newTask, description: e.target.value})}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white transition-all duration-200 resize-none shadow-sm focus:shadow-md hover:shadow-sm"
                    placeholder="Enter task description (optional)"
                  ></textarea>
                </div>

                <div className="flex justify-end space-x-3 pt-2">
                  {editingTask && (
                    <button
                      type="button"
                      onClick={() => {
                        setEditingTask(null);
                        setNewTask({ title: '', description: '', category: '', due_date: '' });
                        setShowCreateForm(false);
                      }}
                      className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors duration-200"
                    >
                      Cancel
                    </button>
                  )}
                  <button
                    type="submit"
                    className="px-6 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-all duration-200 shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
                  >
                    {editingTask ? 'Update Task' : 'Create Task'}
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Two-column responsive layout: Task List + AI Agent */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left column - Task List (2/3 width on large screens) */}
            <div className="lg:col-span-2">
              {/* Tasks Grid - Modern Card Layout */}
              <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">All Tasks</h2>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
              </span>
            </div>

            {loadingTasks ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-1 gap-4">
                {[1, 2, 3].map(i => (
                  <div key={i} className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 animate-pulse">
                    <div className="flex items-center space-x-4">
                      <div className="w-5 h-5 bg-gray-200 dark:bg-gray-700 rounded-full"></div>
                      <div className="flex-1 space-y-3">
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
                        <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
                        <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : tasks.length === 0 ? (
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-12 text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No tasks yet</h3>
                <p className="text-gray-500 dark:text-gray-400 mb-4">Get started by creating your first task</p>
                <button
                  onClick={() => {
                    setEditingTask(null);
                    setNewTask({ title: '', description: '', category: '', due_date: '' });
                    setShowCreateForm(true);
                  }}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                >
                  Create Task
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {tasks.map((task, index) => (
                  <div
                    key={task.id}
                    className={`bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden transition-all duration-200 hover:shadow-md group ${
                      task.completed ? 'opacity-80' : ''
                    }`}
                    style={{
                      animation: 'fadeInUp 0.3s ease-out forwards',
                      animationDelay: `${index * 50}ms`,
                    }}
                  >
                    <div className="p-5">
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-3 flex-1 min-w-0">
                          <button
                            onClick={() => toggleComplete(task.id)}
                            className="flex-shrink-0 mt-0.5"
                          >
                            <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all duration-200 ${
                              task.completed
                                ? 'border-green-500 bg-green-500 dark:border-green-400 dark:bg-green-400'
                                : 'border-gray-300 dark:border-gray-600 group-hover:border-blue-500 dark:group-hover:border-blue-400'
                            }`}>
                              {task.completed && (
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-2.5 w-2.5 text-white dark:text-gray-900" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                </svg>
                              )}
                            </div>
                          </button>

                          <div className="flex-1 min-w-0">
                            <div className="flex items-center justify-between mb-2">
                              <h3 className={`text-sm font-medium ${
                                task.completed
                                  ? 'text-gray-500 dark:text-gray-400 line-through'
                                  : 'text-gray-900 dark:text-white'
                              }`}>
                                {task.title}
                              </h3>
                              <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                                task.completed
                                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                                  : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                              }`}>
                                {task.completed ? 'Completed' : 'Active'}
                              </span>
                            </div>

                            {task.category && task.category.trim() !== '' && (
                              <div className="mb-2">
                                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                                  {task.category}
                                </span>
                              </div>
                            )}

                            {task.description && (
                              <div className="mt-2">
                                <p className={`text-xs p-3 rounded-lg ${
                                  task.completed
                                    ? 'text-gray-400 dark:text-gray-500 bg-gray-50 dark:bg-gray-700/50'
                                    : 'text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/30'
                                }`}>
                                  {task.description}
                                </p>
                              </div>
                            )}

                            <div className="flex flex-wrap items-center gap-2 mt-3 text-xs text-gray-400 dark:text-gray-500">
                              <div className="flex items-center space-x-1">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                </svg>
                                <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                              </div>

                              {task.due_date && (
                                <div className="flex items-center space-x-1">
                                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                  </svg>
                                  <span>Due: {new Date(task.due_date).toLocaleDateString()}</span>
                                </div>
                              )}

                              {task.updated_at !== task.created_at && (
                                <div className="flex items-center space-x-1">
                                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                  </svg>
                                  <span>Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center space-x-2 ml-4 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                          <button
                            onClick={() => handleEdit(task)}
                            className="p-1.5 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                            title="Edit task"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                            </svg>
                          </button>
                          <button
                            onClick={() => handleDelete(task.id)}
                            className="p-1.5 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors duration-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                            title="Delete task"
                          >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        {/* End of left column - Task List */}

        {/* Right column - AI Task Agent (1/3 width on large screens) */}
        <div className="lg:col-span-1">
          <TaskAgentChat onTaskUpdate={fetchTasks} />
        </div>
      </div>
      {/* End of two-column grid */}
    </div>

      <style jsx global>{`
        @keyframes fade-in-up {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fade-in-up {
          animation: fade-in-up 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  );
};

export default TodosPage;