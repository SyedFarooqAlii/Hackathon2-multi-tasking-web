import React from 'react'
import { Todo } from '@/lib/types'
import { Button } from '@/components/ui/Button'

interface TodoItemProps {
  todo: Todo
  onToggleComplete: (id: string, completed: boolean) => void
  onDelete: (id: string) => void
  onEdit: () => void
}

export const TodoItem: React.FC<TodoItemProps> = ({
  todo,
  onToggleComplete,
  onDelete,
  onEdit
}) => {
  return (
    <div
      className={`p-4 rounded-md border flex items-center justify-between ${
        todo.completed
          ? 'bg-green-50 border-green-200 dark:bg-green-900/30 dark:border-green-700'
          : 'bg-white border-gray-200 dark:bg-gray-800 dark:border-gray-700'
      }`}
    >
      <div className="flex items-center">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={(e) => onToggleComplete(todo.id, e.target.checked)}
          className="h-4 w-4 text-indigo-600 rounded mr-3 cursor-pointer"
        />
        <div className="flex flex-col">
          <span className={todo.completed
            ? 'line-through text-gray-500 dark:text-gray-400'
            : 'text-gray-800 dark:text-gray-200'
          }>
            {todo.title}
          </span>
          {todo.description && (
            <span className={`text-sm mt-1 ${todo.completed
              ? 'line-through text-gray-400 dark:text-gray-500'
              : 'text-gray-600 dark:text-gray-300'}`}>
              {todo.description}
            </span>
          )}
        </div>
      </div>
      <div className="flex space-x-2">
        <Button variant="secondary" size="sm" onClick={onEdit}>
          Edit
        </Button>
        <Button variant="danger" size="sm" onClick={() => onDelete(todo.id)}>
          Delete
        </Button>
      </div>
    </div>
  )
}