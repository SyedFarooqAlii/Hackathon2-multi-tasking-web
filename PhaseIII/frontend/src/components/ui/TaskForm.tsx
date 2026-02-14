import React, { useState } from 'react';
import { Input } from './Input';
import { Button } from './Button';

interface TaskFormProps {
  onSubmit: (task: { title: string; description?: string }) => void;
  isLoading?: boolean;
}

export const TaskForm: React.FC<TaskFormProps> = ({ onSubmit, isLoading = false }) => {
  const [task, setTask] = useState({
    title: '',
    description: ''
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setTask(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Simple validation
    const newErrors: Record<string, string> = {};
    if (!task.title.trim()) {
      newErrors.title = 'Task title is required';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onSubmit(task);
    setTask({ title: '', description: '' });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Task Title"
        type="text"
        name="title"
        value={task.title}
        onChange={handleChange}
        error={errors.title}
        placeholder="What needs to be done?"
      />

      <Input
        label="Description"
        type="text"
        name="description"
        value={task.description}
        onChange={handleChange}
        placeholder="Add details (optional)"
      />

      <div className="flex gap-4 pt-2">
        <Button
          type="submit"
          isLoading={isLoading}
          variant="primary"
        >
          Add Task
        </Button>

        <Button
          type="button"
          variant="secondary"
          onClick={() => setTask({ title: '', description: '' })}
          disabled={isLoading}
        >
          Reset
        </Button>
      </div>
    </form>
  );
};