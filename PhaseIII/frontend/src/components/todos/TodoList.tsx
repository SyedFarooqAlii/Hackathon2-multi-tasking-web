'use client'

import React, { useState, useEffect } from 'react'
import { Todo } from '@/lib/types'
import { todoApi } from '@/lib/api'
import { TodoItem } from './TodoItem'
import { TodoForm } from './TodoForm'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'

interface TodoListProps {
  userId: string
}

export const TodoList: React.FC<TodoListProps> = ({ userId }) => {
  const [todos, setTodos] = useState<Todo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null)

  // Fetch todos when component mounts
  useEffect(() => {
    fetchTodos()
  }, [])

  const fetchTodos = async () => {
    try {
      setLoading(true)
      setError('')
      const response = await todoApi.getTodos()
      setTodos(response.tasks)
    } catch (err: any) {
      console.error('Error fetching todos:', err)
      setError(err.message || 'Failed to load todos')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTodo = async (title: string, description?: string) => {
    try {
      const newTodo = await todoApi.createTodo({ title, description })
      setTodos([newTodo, ...todos])
      setShowForm(false)
    } catch (err: any) {
      console.error('Error creating todo:', err)
      setError(err.message || 'Failed to create todo')
    }
  }

  const handleUpdateTodo = async (id: string, updates: Partial<Todo>) => {
    try {
      const updatedTodo = await todoApi.updateTodo(id, updates)
      setTodos(todos.map(todo => todo.id === id ? updatedTodo : todo))
      setEditingTodo(null)
    } catch (err: any) {
      console.error('Error updating todo:', err)
      setError(err.message || 'Failed to update todo')
    }
  }

  const handleDeleteTodo = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        await todoApi.deleteTodo(id)
        setTodos(todos.filter(todo => todo.id !== id))
      } catch (err: any) {
        console.error('Error deleting todo:', err)
        setError(err.message || 'Failed to delete todo')
      }
    }
  }

  const handleToggleComplete = async (id: string, completed: boolean) => {
    try {
      const updatedTodo = await todoApi.toggleTodoCompletion(id, completed)
      setTodos(todos.map(todo => todo.id === id ? updatedTodo : todo))
    } catch (err: any) {
      console.error('Error toggling todo completion:', err)
      setError(err.message || 'Failed to update todo')
    }
  }

  if (loading) {
    return (
      <Card className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          {[1, 2, 3].map((i) => (
            <div key={i} className="space-y-2">
              <div className="h-4 bg-gray-200 rounded"></div>
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            </div>
          ))}
        </div>
      </Card>
    )
  }

  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">Your Todos</h2>
        <Button onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Todo'}
        </Button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {showForm && (
        <div className="mb-6">
          <TodoForm
            onSubmit={handleCreateTodo}
            onCancel={() => setShowForm(false)}
            submitLabel="Add Todo"
          />
        </div>
      )}

      {editingTodo && (
        <div className="mb-6">
          <TodoForm
            initialData={editingTodo}
            onSubmit={(title, description) => handleUpdateTodo(editingTodo.id, { title, description })}
            onCancel={() => setEditingTodo(null)}
            submitLabel="Update Todo"
          />
        </div>
      )}

      {todos.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No todos yet. Add your first todo!</p>
        </div>
      ) : (
        <div className="space-y-3">
          {todos.map(todo => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDeleteTodo}
              onEdit={() => setEditingTodo(todo)}
            />
          ))}
        </div>
      )}
    </Card>
  )
}