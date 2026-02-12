# PhaseIII - Secure Multi-User Todo Web Application

A full-stack web application with secure authentication, real-time chat, and task management capabilities.

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens with Better Auth
- **API Documentation**: OpenAPI/Swagger

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Lucide React icons
- **State Management**: React Context API
- **Forms**: React Hook Form with Zod validation

## Features

- ✅ User authentication (signup/login) with JWT tokens
- ✅ Secure password hashing with bcrypt
- ✅ Per-user task management (CRUD operations)
- ✅ Real-time chat interface
- ✅ Responsive UI design
- ✅ Protected routes and API endpoints
- ✅ CORS configuration for secure cross-origin requests

## Project Structure

```
PhaseIII/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API routes
│   │   │   └── v1/         # API version 1
│   │   │       ├── auth.py # Authentication endpoints
│   │   │       ├── todos.py # Todo CRUD endpoints
│   │   │       └── chat.py # Chat endpoints
│   │   ├── core/           # Core functionality
│   │   │   ├── config.py   # Configuration settings
│   │   │   ├── database.py # Database connection
│   │   │   └── security.py # JWT & password hashing
│   │   ├── models/         # SQLModel data models
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js App Router pages
│   │   │   ├── auth/      # Authentication pages
│   │   │   ├── dashboard/ # Dashboard page
│   │   │   └── todos/     # Todo management page
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   ├── lib/           # Utility functions
│   │   └── types/         # TypeScript types
│   ├── package.json       # Node dependencies
│   └── .env.example       # Environment variables template
│
└── README.md              # This file
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL database (Neon recommended)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from template:
```bash
cp .env.example .env
```

5. Configure environment variables in `.env`:
```env
NEON_DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=your-super-secret-jwt-signing-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. Run the backend server:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file from template:
```bash
cp .env.example .env.local
```

4. Configure environment variables in `.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXTAUTH_SECRET=your-super-secret-jwt-signing-key
NEXTAUTH_URL=http://localhost:3000
```

5. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user (protected)

### Todos
- `GET /api/v1/todos` - Get all todos for current user (protected)
- `POST /api/v1/todos` - Create new todo (protected)
- `GET /api/v1/todos/{id}` - Get specific todo (protected)
- `PUT /api/v1/todos/{id}` - Update todo (protected)
- `DELETE /api/v1/todos/{id}` - Delete todo (protected)

### Chat
- `POST /api/v1/chat` - Send chat message (protected)

## Security Features

- **Password Hashing**: Bcrypt with salt rounds
- **JWT Tokens**: Secure token-based authentication
- **CORS Protection**: Configured allowed origins
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Prevention**: SQLModel ORM with parameterized queries
- **Per-User Data Isolation**: All queries filtered by authenticated user ID

## Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `email` (String, Unique)
- `username` (String, Unique)
- `hashed_password` (String)
- `created_at` (DateTime)

### Todos Table
- `id` (UUID, Primary Key)
- `title` (String)
- `description` (String, Optional)
- `completed` (Boolean)
- `user_id` (UUID, Foreign Key)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Development

### Running Tests

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Building for Production

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd frontend
npm run build
npm start
```

## Environment Variables

### Backend (.env)
- `NEON_DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `ALGORITHM` - JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `BACKEND_CORS_ORIGINS` - Allowed CORS origins

### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE_URL` - Backend API URL
- `NEXTAUTH_SECRET` - NextAuth secret key
- `NEXTAUTH_URL` - Frontend application URL

## Troubleshooting

### Backend Issues

**Database connection errors:**
- Verify `NEON_DATABASE_URL` is correct
- Check database is accessible
- Ensure IP is whitelisted in Neon dashboard

**JWT token errors:**
- Ensure `SECRET_KEY` matches between backend and frontend
- Check token expiration settings

### Frontend Issues

**API connection errors:**
- Verify `NEXT_PUBLIC_API_BASE_URL` points to running backend
- Check CORS settings in backend
- Ensure backend is running on correct port

**Authentication errors:**
- Clear browser cookies and local storage
- Verify JWT token is being sent in Authorization header

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of Hackathon Phase III.

## Support

For issues and questions, please open an issue on GitHub.
