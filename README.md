HEAD
# Group Study Finder

A comprehensive web application for students to find study partners, form study groups, and collaborate effectively for academic success. Built with Flask and Vue.js.

## 🚀 Features

### 🔐 Authentication & User Management
- User registration with role selection (student/teacher)
- Secure login/logout with session management
- Profile editing with password changes
- Course management (add/remove courses doing/done)

### 👥 Study Groups
- Create study groups with course selection
- Session scheduling (start/end times)
- Join request system with approval/rejection
- Group member management with leader/member roles
- Real-time group chat

### 💬 Real-time Communication
- Global chat for all users
- Group-specific chat rooms
- Socket.IO integration for live messaging
- Connection status indicators

### 📚 Course System
- Course creation (teachers only)
- Course search and filtering
- Course feedback and ratings
- User course tracking (doing/done status)

### 🔔 Notifications
- Notification system for group activities
- Join request notifications
- Exam alert generation
- Resource request functionality
- Mark as read/unread functionality

### 🔍 User Discovery
- Search users by course and completion status
- Find study partners based on common courses
- Contact users via email integration

### 📊 Dashboard
- Personalized user dashboard
- Quick stats (courses, groups, notifications)
- Quick action buttons for common tasks
- Recent activity overview

## 🏗️ Technology Stack

### Backend (Flask)
- **Framework**: Flask 2.3.3
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Flask-Login with session management
- **Real-time**: Socket.IO for live chat
- **API**: RESTful API with JSON responses
- **Architecture**: MVC pattern with blueprints

### Frontend (Vue.js)
- **Framework**: Vue 3.3.4
- **State Management**: Vuex 4.0.2
- **Routing**: Vue Router 4.2.4
- **UI Framework**: Bootstrap 5.3.0
- **Real-time**: Socket.IO client
- **Icons**: Font Awesome 6.4.2

### Database
- **Database**: MySQL 8.0+
- **ORM**: SQLAlchemy
- **Migrations**: Flask-Migrate

## 📋 Prerequisites

- Python 3.8+ with pip
- Node.js 14+ with npm
- MySQL 8.0+

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "470 project"
```

### 2. Database Setup
```bash
# Create database
mysql -u root -p < database/schema.sql

# Insert sample data (optional)
mysql -u root -p < database/sample_data.sql
```

### 3. Backend Setup
```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_CONFIG=development
export DATABASE_URL="mysql+pymysql://root:your_password@localhost/group_study_finder"

# Initialize database
python run.py init-db

# Run the Flask server
python run.py
```

### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run serve
```

### 5. Access the Application
- Frontend: http://localhost:8080
- Backend API: http://localhost:5000/api

## 📁 Project Structure

```
470 project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── controllers/        # API endpoints
│   │   ├── models/            # Database models
│   │   └── static/uploads/    # File uploads
│   ├── config.py             # Configuration
│   ├── run.py               # Application entry point
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable Vue components
│   │   ├── views/          # Page components
│   │   ├── router/         # Vue Router configuration
│   │   ├── store/          # Vuex state management
│   │   └── services/       # API services
│   ├── package.json        # Node.js dependencies
│   └── vue.config.js      # Vue CLI configuration
├── database/
│   ├── schema.sql         # Database schema
│   └── sample_data.sql    # Sample data
└── README.md
```

## 🔄 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/check-auth` - Check authentication status

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update profile
- `PUT /api/users/change-password` - Change password
- `GET /api/users/search` - Search users by course

### Courses
- `GET /api/courses/` - Get all courses
- `POST /api/courses/` - Create course (teachers only)
- `GET /api/courses/search` - Search courses
- `GET /api/courses/{id}/feedback` - Get course feedback

### Groups
- `GET /api/groups/` - Get study groups
- `POST /api/groups/` - Create study group
- `GET /api/groups/{id}` - Get group details
- `POST /api/groups/{id}/join-request` - Request to join group

### Chat
- `GET /api/chat/global` - Get global messages
- `POST /api/chat/global` - Send global message
- `GET /api/chat/group/{id}` - Get group messages
- `POST /api/chat/group/{id}` - Send group message

## 🚀 Deployment

### Production Configuration

**Environment Variables**:
```bash
export FLASK_CONFIG=production
export DATABASE_URL="mysql+pymysql://username:password@host:port/database"
export SECRET_KEY="your-secret-key"
```

**Build Frontend**:
```bash
cd frontend
npm run build


## 📝 License

This project is licensed under the MIT License- dunno what that is - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Development

- **Project**: CSE470 - Software Engineering
- **Institution**: BRAC University
- **Academic Year**: 2025

## 🐛 Known Issues

- File upload functionality is planned for future releases
- Notifications not complete

## 📞 Support

For support, email am.shahamat.nurain@g.bracu.ac.bd or create an issue in the repository.

---

**Happy Studying! 📚✨**

# Group_Study_Finder
cse470 project webapp where groups on unis study together
origin/main
