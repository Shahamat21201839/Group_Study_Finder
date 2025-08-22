@echo off
REM Group Study Finder - Easy Startup Script for Windows

echo 🚀 Group Study Finder - Starting Application
echo ===========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if Node.js is installed  
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 14+
    pause
    exit /b 1
)

echo ✅ Prerequisites found!

REM Setup backend
echo 🔧 Setting up backend...
cd backend

if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

echo ⚡ Activating virtual environment...
call venv\Scripts\activate.bat

if not exist ".env" (
    echo ⚙️ Creating .env file...
    copy .env.example .env
    echo ⚠️ Please edit backend\.env with your MySQL credentials!
)

echo 📦 Installing Python dependencies...
pip install -r requirements.txt >nul 2>&1

echo 🗃️ Initializing database...
python run.py init-db

echo 🎯 Starting backend server...
start "Backend Server" python run.py

cd ..

REM Setup frontend
echo 🎨 Setting up frontend...
cd frontend

if not exist "node_modules" (
    echo 📦 Installing Node.js dependencies...
    npm install >nul 2>&1
)

echo 🎯 Starting frontend server...
start "Frontend Server" npm run serve

cd ..

echo.
echo 🎉 Group Study Finder is starting up!
echo ==================================
echo 📱 Frontend: http://localhost:8080
echo 🔗 Backend API: http://localhost:5000
echo.
echo 💡 Check the opened terminal windows for server status
echo 🛑 Close terminal windows to stop servers

pause
