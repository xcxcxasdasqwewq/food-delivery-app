#!/bin/bash

echo "🍔 Starting Food Delivery App..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Setup backend
echo "📦 Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# Initialize database and seed data
echo "🗄️  Initializing database..."
python3 -c "from app import init_db; init_db()"
python3 seed_data.py

echo "✅ Backend setup complete!"
echo ""

# Setup frontend
echo "📦 Setting up frontend..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies (this may take a few minutes)..."
    npm install
fi

echo "✅ Frontend setup complete!"
echo ""

# Start backend in background
echo "🚀 Starting backend server..."
cd ../backend
source venv/bin/activate
python3 app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"
echo ""

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "🚀 Starting frontend server..."
cd ../frontend
npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"
echo ""

echo "✅ Food Delivery App is running!"
echo ""
echo "📍 Backend: http://127.0.0.1:5001"
echo "📍 Frontend: http://localhost:3000"
echo ""
echo "📝 Test Accounts:"
echo "   Admin:     username=admin,      password=admin123"
echo "   Restaurant: username=rest1,     password=rest123"
echo "   Delivery:   username=delivery1,  password=delivery123"
echo "   Customer:   username=customer1,  password=customer123"
echo ""
echo "📋 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop the servers, run: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop..."

# Wait for user interrupt
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait

