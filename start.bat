@echo off
echo 🍔 Starting Food Delivery App...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3 first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Setup backend
echo 📦 Setting up backend...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -q -r requirements.txt

REM Initialize database and seed data
echo 🗄️  Initializing database...
python -c "from app import init_db; init_db()"
python seed_data.py

echo ✅ Backend setup complete!
echo.

REM Setup frontend
echo 📦 Setting up frontend...
cd ..\frontend
if not exist "node_modules" (
    echo Installing frontend dependencies (this may take a few minutes)...
    call npm install
)

echo ✅ Frontend setup complete!
echo.

REM Start backend in background
echo 🚀 Starting backend server...
cd ..\backend
call venv\Scripts\activate.bat
start "Backend Server" python app.py

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo 🚀 Starting frontend server...
cd ..\frontend
start "Frontend Server" npm start

echo.
echo ✅ Food Delivery App is running!
echo.
echo 📍 Backend: http://127.0.0.1:5001
echo 📍 Frontend: http://localhost:3000
echo.
echo 📝 Test Accounts:
echo    Admin:     username=admin,      password=admin123
echo    Restaurant: username=rest1,     password=rest123
echo    Delivery:   username=delivery1,  password=delivery123
echo    Customer:   username=customer1,  password=customer123
echo.
echo 🛑 Close the command windows to stop the servers.
echo.
pause

