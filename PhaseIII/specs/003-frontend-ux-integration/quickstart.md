# Quickstart Guide: Frontend UX & API Client Integration

## Overview
This guide provides the essential information needed to set up, develop, and deploy the frontend application for the secure multi-user todo web application.

## Prerequisites
- **Node.js**: Version 18.0 or higher
- **Package Manager**: Yarn (recommended) or npm
- **Backend API**: Access to the running backend server
- **Git**: Version control system
- **Text Editor**: VS Code with recommended extensions

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd frontend
```

### 2. Install Dependencies
```bash
# Using Yarn (recommended)
yarn install

# Or using npm
npm install
```

### 3. Environment Variables
Copy the example environment file and update the values:

```bash
cp .env.example .env.local
```

Required environment variables:
```
# Backend API configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1

# Authentication configuration
NEXTAUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000

# Database configuration (if using local auth)
DATABASE_URL=your-database-url
```

## Development Workflow

### 1. Starting the Development Server
```bash
# Start the development server
yarn dev

# Or with npm
npm run dev

# The application will be available at http://localhost:3000
```

### 2. Project Structure
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication-related pages
│   ├── (protected)/       # Protected routes
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── middleware.ts      # Route protection
├── components/            # Reusable React components
│   ├── auth/             # Authentication components
│   ├── todos/            # Todo management components
│   └── ui/               # UI primitive components
├── lib/                  # Utility functions and API client
│   ├── api.ts            # API client implementation
│   ├── auth.ts           # Authentication helpers
│   ├── types.ts          # TypeScript type definitions
│   └── utils.ts          # Helper functions
├── hooks/                # Custom React hooks
├── providers/            # React context providers
├── public/               # Static assets
├── styles/               # Global styles
└── package.json          # Dependencies and scripts
```

### 3. Adding New Features
1. **Create feature branch**: `git checkout -b feature/descriptive-name`
2. **Follow component architecture**: Add components to appropriate directories
3. **Maintain type safety**: Use TypeScript interfaces consistently
4. **Test thoroughly**: Ensure new features work with authentication
5. **Commit changes**: Use conventional commit messages

## Key Development Commands

### Development
```bash
yarn dev              # Start development server
yarn build            # Build for production
yarn start            # Start production server
yarn lint             # Run linter
yarn type-check       # Run TypeScript compiler
```

### Testing
```bash
yarn test             # Run all tests
yarn test:watch       # Run tests in watch mode
yarn test:coverage    # Run tests with coverage report
```

### Code Quality
```bash
yarn format           # Format code with Prettier
yarn lint:fix         # Fix linting issues automatically
```

## Authentication Flow

### 1. User Registration
- Navigate to `/register`
- Fill in registration form
- Submit to create new account
- Automatically logged in after registration

### 2. User Login
- Navigate to `/login`
- Enter credentials
- Authenticate with backend API
- JWT token stored securely in browser

### 3. Protected Routes
- Access to `/dashboard`, `/todos` requires authentication
- Middleware redirects unauthenticated users to login
- Session state managed by Better Auth

## API Client Usage

### Making Authenticated Requests
```typescript
import { apiClient } from '@/lib/api';

// Get user's todos
const todos = await apiClient.getTodos();

// Create a new todo
const newTodo = await apiClient.createTodo({
  title: 'New todo',
  description: 'Todo description'
});

// Update a todo
const updatedTodo = await apiClient.updateTodo(todoId, {
  title: 'Updated title',
  completed: true
});
```

### Error Handling
```typescript
try {
  const todos = await apiClient.getTodos();
} catch (error) {
  if (error.status === 401) {
    // Handle unauthorized access
    // User will be redirected to login
  } else {
    // Handle other errors
    console.error('Error fetching todos:', error);
  }
}
```

## Component Development

### Creating New Components
```typescript
// components/ui/Button.tsx
import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  onClick?: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  onClick,
  disabled = false
}) => {
  // Implementation
};
```

### Using Custom Hooks
```typescript
// hooks/useTodos.ts
import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

export const useTodos = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Implementation
};
```

## Deployment

### 1. Build for Production
```bash
yarn build
```

### 2. Environment Variables for Production
Ensure these variables are set in your hosting environment:
```
NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.com/api/v1
NEXTAUTH_SECRET=your-production-secret
NEXTAUTH_URL=https://your-frontend-domain.com
```

### 3. Platform-Specific Deployment

#### Vercel
```bash
# Deploy to Vercel
vercel --prod
```

#### Netlify
```bash
# Build command
yarn build

# Publish directory
out/
```

#### Traditional Hosting
```bash
# Build and serve with Node.js
yarn build
yarn start
```

## Troubleshooting

### Common Issues

**Issue**: Authentication not working
**Solution**: Verify NEXTAUTH_SECRET is set correctly in environment

**Issue**: API calls failing
**Solution**: Check NEXT_PUBLIC_API_BASE_URL points to running backend

**Issue**: Styles not loading
**Solution**: Ensure Tailwind CSS is properly configured

**Issue**: Type errors
**Solution**: Run `yarn type-check` to identify specific issues

### Debugging Tips
- Enable Next.js debug mode: `NEXT_DEBUG=1`
- Check browser console for client-side errors
- Verify backend API is running and accessible
- Use React Developer Tools for component debugging

## Performance Optimization

### Bundle Size
- Use dynamic imports for heavy components
- Implement code splitting for routes
- Optimize images and assets

### Loading States
- Implement skeleton screens
- Use optimistic updates where appropriate
- Cache API responses when possible

## Security Best Practices

### Authentication Security
- Store JWT tokens securely (avoid localStorage for sensitive tokens)
- Implement token refresh mechanisms
- Use HTTPS in production

### Input Validation
- Validate all user inputs on frontend and backend
- Sanitize user-generated content
- Prevent XSS and injection attacks

This quickstart guide provides the essential information needed to begin development on the frontend application. For more detailed information about specific components or features, refer to the respective documentation files.