#!/bin/bash

# Group Study Finder - Easy Startup Script

echo "🚀 Group Study Finder - Starting Application"
echo "==========================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 14+"
    exit 1
fi

if ! command_exists mysql; then
    echo "❌ MySQL is not installed. Please install MySQL 8.0+"
    exit 1
fi

echo "✅ All prerequisites found!"

# Check if database schema exists
echo "📊 Checking database setup..."
if [ ! -f "database/schema.sql" ]; then
    echo "❌ Database schema not found!"
    exit 1
fi

echo "✅ Database schema found!"

# Setup backend
echo "🔧 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "⚡ Activating virtual environment..."
source venv/bin/activate

if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your MySQL credentials!"
fi

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo "🗃️ Initializing database..."
python run.py init-db

echo "🎯 Starting backend server..."
python run.py &
BACKEND_PID=$!

cd ..

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install > /dev/null 2>&1
fi

echo "🎯 Starting frontend server..."
npm run serve &
FRONTEND_PID=$!

cd ..

echo ""
echo "🎉 Group Study Finder is starting up!"
echo "=================================="
echo "📱 Frontend: http://localhost:8080"
echo "🔗 Backend API: http://localhost:5000"
echo ""
echo "🛑 Press Ctrl+C to stop all servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ All servers stopped. Goodbye!"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for processes
wait
