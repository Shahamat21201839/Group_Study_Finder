# Group Study Finder - Complete Setup Guide

## 📋 Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.8+** with pip: https://python.org/downloads/
- **Node.js 14+** with npm: https://nodejs.org/download/
- **MySQL 8.0+**: https://dev.mysql.com/downloads/

## 🚀 Quick Start (Recommended)

### 1. Database Setup
```bash
# Start MySQL service (Windows: through services, Mac: brew services start mysql)
mysql -u root -p

# In MySQL console, create database:
CREATE DATABASE IF NOT EXISTS group_study_finder;
USE group_study_finder;
exit;

# Run the schema file
mysql -u root -p < database/schema.sql
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment (highly recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env file with your MySQL credentials:
# Change DATABASE_URL to match your MySQL setup
# Default: mysql+pymysql://root:password@localhost/group_study_finder

# Initialize database
python run.py init-db

# Start backend server
python run.py
```

### 3. Frontend Setup (New Terminal)
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run serve
```

### 4. Setup Sample Data (Optional but Recommended)
```bash
# From project root directory
python setup_sample_data.py
```

### 5. Access Application
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5000/api

## 👤 Test Accounts

After running the sample data script:

- **Teacher**: john.smith@bracu.ac.bd / password123
- **Students**: 
  - alice.j@g.bracu.ac.bd / password123
  - bob.w@g.bracu.ac.bd / password123  
  - carol.d@g.bracu.ac.bd / password123
  - david.b@g.bracu.ac.bd / password123

## 🏗️ Project Structure

```
470 project/
├── backend/                    # Flask Backend
│   ├── app/
│   │   ├── __init__.py        # App factory
│   │   ├── controllers/       # API endpoints (MVC Controllers)
│   │   │   ├── auth_controller.py
│   │   │   ├── user_controller.py
│   │   │   ├── course_controller.py
│   │   │   ├── group_controller.py
│   │   │   ├── chat_controller.py
│   │   │   └── notification_controller.py
│   │   ├── models/           # Database models (MVC Models)
│   │   │   ├── user.py
│   │   │   ├── course.py
│   │   │   ├── group_study.py
│   │   │   └── [other models]
│   │   └── static/uploads/   # File upload directory
│   ├── config.py            # Configuration
│   ├── run.py              # Application entry point
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/               # Vue.js Frontend
│   ├── src/
│   │   ├── components/    # Reusable Vue components
│   │   ├── views/        # Page components (MVC Views)
│   │   ├── router/       # Vue Router configuration
│   │   ├── store/        # Vuex state management
│   │   └── services/     # API service layer
│   ├── package.json      # Node.js dependencies
│   └── vue.config.js     # Vue CLI configuration
├── database/
│   ├── schema.sql        # Database schema
│   └── sample_data.sql   # Sample data (legacy)
├── setup_sample_data.py  # Python script for sample data
└── README.md
```

## 🔧 Features Implemented

### ✅ Authentication & User Management
- User registration with role selection (student/teacher)
- Secure login/logout with session management
- Profile editing with password changes
- Course management (add/remove courses doing/done)

### ✅ Study Groups
- Create study groups with course selection
- Session scheduling (start/end times)
- Join request system with approval/rejection
- Group member management with leader/member roles
- Group details and management

### ✅ Real-time Communication
- Global chat for all users
- Group-specific chat rooms  
- Socket.IO integration for live messaging
- Connection status indicators

### ✅ Course System
- Course creation (teachers only)
- Course search and filtering
- Course feedback and ratings
- User course tracking (doing/done status)

### ✅ User Discovery & Search
- Search users by course and completion status
- Find study partners based on common courses
- Contact functionality

### ✅ Notifications
- Notification system for group activities
- Join request notifications
- Mark as read/unread functionality

### ✅ Dashboard
- Personalized user dashboard with stats
- Quick action buttons for common tasks
- Recent activity overview

## 🔄 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/check-auth` - Check authentication

### Users  
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update profile
- `PUT /api/users/change-password` - Change password
- `GET /api/users/search` - Search users by course

### Courses
- `GET /api/courses/` - Get all courses
- `POST /api/courses/` - Create course (teachers)
- `GET /api/courses/search` - Search courses
- `GET /api/courses/{id}/feedback` - Course feedback

### Groups
- `GET /api/groups/` - Get study groups
- `POST /api/groups/` - Create study group  
- `GET /api/groups/{id}` - Get group details
- `GET /api/groups/my-groups` - Get user's groups
- `POST /api/groups/{id}/join-request` - Request to join
- `GET /api/groups/{id}/join-requests` - View requests (leaders)
- `PUT /api/groups/join-requests/{id}/respond` - Approve/reject

### Chat
- `GET /api/chat/global` - Get global messages
- `POST /api/chat/global` - Send global message
- `GET /api/chat/group/{id}` - Get group messages
- `POST /api/chat/group/{id}` - Send group message

### Notifications
- `GET /api/notifications/` - Get notifications
- `PUT /api/notifications/{id}/read` - Mark as read

## 🛠️ Troubleshooting

### Common Issues:

1. **Database Connection Error**
   ```
   Error: Can't connect to MySQL server
   ```
   - Check if MySQL is running
   - Verify credentials in `.env` file
   - Ensure database exists

2. **Module Not Found Error**
   ```
   ModuleNotFoundError: No module named 'flask'
   ```
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt`

3. **Port Already in Use**
   ```
   OSError: [Errno 48] Address already in use
   ```
   - Frontend: Change port in `vue.config.js`
   - Backend: Change port in `run.py`

4. **CORS Issues**
   - Ensure `CORS_ORIGINS` in `.env` matches frontend URL
   - Check if backend is running on correct port

5. **Sample Data Not Loading**
   - Make sure database schema is created first
   - Check MySQL credentials
   - Verify virtual environment is activated

### Development Tips:

- Always activate virtual environment before working on backend
- Use `python run.py reset-db` to reset database if needed
- Frontend runs on http://localhost:8080 by default
- Backend runs on http://localhost:5000 by default
- Check browser console for frontend errors
- Check terminal for backend errors

## 📱 Mobile Responsiveness

The application is fully responsive and works on:
- Desktop browsers
- Tablets  
- Mobile devices
- Uses Bootstrap 5 for responsive design

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CORS protection
- SQL injection prevention through SQLAlchemy
- Input validation and sanitization

## 🚀 Production Deployment

For production deployment:

1. **Environment Variables**
   ```bash
   FLASK_CONFIG=production
   SECRET_KEY=your-secure-secret-key
   DATABASE_URL=your-production-db-url
   ```

2. **Build Frontend**
   ```bash
   cd frontend
   npm run build
   ```

3. **Use Production Server**
   - Gunicorn for Flask backend
   - Nginx for static files and reverse proxy
   - SSL certificates for HTTPS

## 📞 Support

- Check documentation in README.md
- Review error messages in terminal/console
- Ensure all prerequisites are installed
- Verify database connection and schema

---

**Happy Coding! 🎓✨**
