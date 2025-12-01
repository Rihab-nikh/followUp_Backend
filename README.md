# FollowUp Backend API

A comprehensive Flask backend API for the FollowUp meeting management application. This RESTful API provides authentication, CRUD operations, AI integration, and analytics for a modern meeting management platform.

## 🚀 Features

### Core Features
- **JWT Authentication** with access/refresh token system
- **User Management** with roles and preferences
- **Meeting Management** with CRUD operations and scheduling
- **Task Management** with Kanban board support
- **Notification System** with auto-generation
- **Dashboard Analytics** with KPI calculations
- **AI Assistant Integration** with Google Gemini API

### Technical Features
- **MongoDB** with optimized indexing
- **Flask Blueprints** for modular architecture
- **Marshmallow** validation schemas
- **CORS** support for frontend integration
- **Rate Limiting** for API protection
- **Comprehensive Error Handling**
- **Request/Response Logging**
- **Multi-language Support** (English/French)

## 📋 Project Structure

```
followup-backend/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration management
│   ├── models/                  # MongoDB data models
│   │   ├── user.py              # User model
│   │   ├── meeting.py           # Meeting model
│   │   ├── task.py              # Task model
│   │   ├── notification.py      # Notification model
│   │   ├── ai_chat.py           # AI chat model
│   │   └── kpi.py               # KPI analytics model
│   ├── schemas/                 # Data validation schemas
│   │   ├── user_schema.py       # User validation
│   │   ├── meeting_schema.py    # Meeting validation
│   │   ├── task_schema.py       # Task validation
│   │   ├── notification_schema.py
│   │   ├── ai_chat_schema.py
│   │   ├── dashboard_schema.py
│   │   └── __init__.py
│   ├── controllers/             # Business logic
│   │   ├── auth_controller.py   # Authentication
│   │   ├── meeting_controller.py
│   │   ├── task_controller.py
│   │   ├── notification_controller.py
│   │   ├── ai_controller.py
│   │   ├── dashboard_controller.py
│   │   └── settings_controller.py
│   ├── routes/                  # API endpoints
│   │   ├── auth_routes.py       # Authentication routes
│   │   ├── meeting_routes.py
│   │   ├── task_routes.py
│   │   ├── notification_routes.py
│   │   ├── ai_routes.py
│   │   ├── dashboard_routes.py
│   │   └── settings_routes.py
│   ├── middleware/              # Request processing
│   │   ├── auth_middleware.py   # JWT authentication
│   │   ├── error_handler.py     # Global error handling
│   │   ├── cors_middleware.py   # CORS configuration
│   │   ├── logging_middleware.py
│   │   ├── rate_limiter.py      # Rate limiting
│   │   └── __init__.py
│   ├── services/                # Business services
│   │   ├── email_service.py     # Email notifications
│   │   ├── notification_service.py
│   │   ├── gemini_service.py    # AI integration
│   │   └── analytics_service.py
│   └── utils/                   # Utility functions
│       ├── db.py                # MongoDB connection
│       ├── jwt_helper.py        # JWT utilities
│       ├── password_helper.py   # Password hashing
│       └── validators.py        # Input validation
├── tests/                       # Test suite
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── run.py                       # Application entry point
└── README.md                    # Documentation
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- MongoDB (local or MongoDB Atlas)
- Redis (optional, for rate limiting)

### Setup Steps

1. **Clone and setup virtual environment:**
```bash
cd followup-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Setup MongoDB:**
```bash
# Local MongoDB
mongod --dbpath /path/to/data

# OR use MongoDB Atlas (update MONGO_URI in .env)
```

5. **Run the application:**
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 🔑 Environment Configuration

### Required Variables
```bash
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
DEBUG=True

# Database
MONGO_URI=mongodb://localhost:27017/followup_db

# JWT Authentication
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=900  # 15 minutes
JWT_REFRESH_TOKEN_EXPIRES=604800  # 7 days

# Gemini AI Integration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-flash

# Frontend CORS
# Use a comma-separated list for multiple allowed origins
# Example:
# FRONTEND_ORIGINS=http://localhost:3000,https://v0-extractedfrontend.vercel.app
FRONTEND_ORIGINS=http://localhost:3000,https://v0-extractedfrontend.vercel.app
```

### Optional Variables
```bash
# Email Configuration (for password reset)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_STORAGE_URL=redis://localhost:6379
```

## 📚 API Endpoints

### Authentication Endpoints
```
POST   /api/auth/register          # Register new user
POST   /api/auth/login             # Login user
POST   /api/auth/refresh           # Refresh access token
POST   /api/auth/logout            # Logout user
GET    /api/auth/me                # Get current user profile
PUT    /api/auth/me                # Update user profile
PUT    /api/auth/password          # Change password
```

### Meeting Endpoints
```
GET    /api/meetings               # Get all meetings (with filters)
GET    /api/meetings/:id           # Get single meeting
POST   /api/meetings               # Create new meeting
PUT    /api/meetings/:id           # Update meeting
DELETE /api/meetings/:id           # Delete meeting
GET    /api/meetings/upcoming      # Get upcoming meetings
GET    /api/meetings/today         # Get today's meetings
GET    /api/meetings/calendar      # Get calendar view
PATCH  /api/meetings/:id/status    # Update meeting status
```

### Task Endpoints
```
GET    /api/tasks                  # Get all tasks (with filters)
GET    /api/tasks/:id              # Get single task
POST   /api/tasks                  # Create new task
PUT    /api/tasks/:id              # Update task
DELETE /api/tasks/:id              # Delete task
PATCH  /api/tasks/:id/status       # Update task status (Kanban)
GET    /api/tasks/upcoming         # Get upcoming tasks
GET    /api/tasks/today            # Get today's tasks
```

### Notification Endpoints
```
GET    /api/notifications          # Get all notifications
GET    /api/notifications/unread   # Get unread count
POST   /api/notifications          # Create notification
PATCH  /api/notifications/:id/read # Mark as read
PATCH  /api/notifications/mark-all-read
DELETE /api/notifications/:id      # Delete notification
```

### AI Assistant Endpoints
```
POST   /api/ai/chat                # Chat with AI assistant
GET    /api/ai/history             # Get chat history
DELETE /api/ai/history/:session_id # Delete chat session
```

### Dashboard Endpoints
```
GET    /api/dashboard/kpis         # Get KPI metrics
GET    /api/dashboard/chart-data   # Get chart data
GET    /api/dashboard/recent-meetings
GET    /api/dashboard/upcoming-tasks
```

### Settings Endpoints
```
GET    /api/settings               # Get user settings
PUT    /api/settings               # Update settings
PUT    /api/settings/language      # Update language
PUT    /api/settings/theme         # Update theme
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login**: POST `/api/auth/login` returns `access_token` and `refresh_token`
2. **Authorization**: Include `Authorization: Bearer <token>` in requests
3. **Token Refresh**: POST `/api/auth/refresh` to get new access token
4. **Protected Routes**: All endpoints except login/register require valid token

### Token Details
- **Access Token**: 15 minutes expiry (configurable)
- **Refresh Token**: 7 days expiry (configurable)
- **Validation**: Automatic middleware validation on all protected routes

## 🤖 AI Integration

### Google Gemini API
- **Purpose**: Intelligent assistant for meeting management help
- **Features**: Context-aware responses, multi-language support
- **Rate Limiting**: 10 requests per minute
- **Security**: API key stored in environment variables

### AI Capabilities
- Meeting scheduling guidance
- Task management help
- Feature navigation assistance
- French/English language support
- Context preservation across chat sessions

## 📊 Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  email: String (unique),
  password: String (hashed),
  full_name: String,
  role: String ("admin" | "user"),
  avatar_initials: String,
  preferences: {
    language: String,
    theme: String,
    notifications: Boolean,
    email_reminders: Boolean
  },
  created_at: DateTime,
  updated_at: DateTime,
  last_login: DateTime
}
```

### Meetings Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  company: String,
  contact: String,
  subject: String,
  description: String,
  date: String (YYYY-MM-DD),
  time: String (HH:MM AM/PM),
  duration: Number,
  location: String,
  status: String ("scheduled" | "completed" | "cancelled"),
  priority: String ("high" | "medium" | "low"),
  notes: String,
  attendees: Array,
  tags: Array,
  phone: String,
  email: String,
  company_address: String,
  created_at: DateTime,
  updated_at: DateTime
}
```

### Tasks Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  title: String,
  description: String,
  meeting_id: ObjectId,
  assignee: String,
  assignee_user_id: ObjectId,
  due_date: String (YYYY-MM-DD),
  priority: String ("high" | "medium" | "low"),
  status: String ("todo" | "inprogress" | "done"),
  tags: Array,
  created_at: DateTime,
  updated_at: DateTime,
  completed_at: DateTime
}
```

## 🔧 Development

### Database Indexes
The application automatically creates optimized indexes for:
- User email lookup
- Meeting date and status filtering
- Task status and due date queries
- Notification read status
- Full-text search across meeting fields

### Rate Limiting
- **Auth endpoints**: 5 requests per minute
- **AI endpoints**: 10 requests per minute  
- **General endpoints**: 100 requests per minute
- Configurable via environment variables

### Error Handling
- Consistent JSON error responses
- Proper HTTP status codes
- Comprehensive logging
- Validation error details

### Security Features
- JWT token authentication
- Password hashing with bcrypt (12 salt rounds)
- Input validation and sanitization
- CORS configuration
- Rate limiting
- NoSQL injection prevention

## 🚀 Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use secure `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configure MongoDB Atlas or secure MongoDB instance
- [ ] Set up Redis for distributed rate limiting
- [ ] Configure email service for password reset
- [ ] Set up SSL/HTTPS
- [ ] Configure proper logging
- [ ] Set up monitoring and health checks

### Deployment Options
1. **Heroku**: Use provided Procfile and environment variables
2. **AWS/GCP**: Deploy with Docker containers
3. **Traditional VPS**: Use Gunicorn with Nginx
4. **Railway/Render**: Simple deployment with environment configuration

## 📝 API Documentation

### Swagger/OpenAPI
The API includes Swagger documentation accessible at `/apidocs/`

### Postman Collection
Import the provided Postman collection for comprehensive API testing.

### Example Responses

#### Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Operation successful"
}
```

#### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "status": 400
}
```

#### Paginated Response
```json
{
  "success": true,
  "data": [ /* array of items */ ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation
- Review the error logs
- Contact the development team

---

**FollowUp Backend API** - Built with Flask, MongoDB, and modern web technologies.
#   f o l l o w U p _ B a c k e n d  
 