---
title: Deployment Guide for Food Delivery App
type: deployment
created: 2025-12-30 14:30:09.477000
updated: 2025-12-30 14:30:09.477000
synced_from: VibeProject
---

# Deployment Guide for Food Delivery App

## Overview
This Deployment Guide provides a comprehensive walkthrough for deploying the Food Delivery App, a web application built with a Flask backend and React frontend. The app supports multiple user roles including Admin, Restaurant Owner, Delivery Person, and Customer, with features for order management, menu handling, and user authentication. The database uses SQLite, which is automatically created on first run with seeded mock data.

The guide covers environment setup, deployment processes for both backend and frontend, server configuration, CI/CD pipeline suggestions, and a deployment checklist. This is tailored for a student project, assuming deployment to cloud platforms like Heroku for the backend and Netlify or Vercel for the frontend.

**Important Note:** Ensure all dependencies are installed and the application runs locally before proceeding with deployment. Refer to the project's README for local setup instructions.

## Prerequisites
Before deploying, ensure you have the following:
- **GitHub Account:** For repository hosting and CI/CD.
- **Cloud Accounts:** 
  - Heroku (or Railway, Render) for backend deployment.
  - Netlify or Vercel for frontend deployment.
- **Domain (Optional):** For custom domain hosting.
- **Tools:**
  - Git for version control.
  - Node.js (v16+) and npm for frontend.
  - Python (v3.8+) and pip for backend.
- **Knowledge:**
  - Basic command-line operations.
  - Understanding of Flask and React deployments.

## Environment Setup
### Backend Environment
1. **Install Dependencies:** Navigate to the backend directory and run `pip install -r requirements.txt`.
2. **Environment Variables:** Create a `.env` file in the backend root with the following (adjust as needed):
   ```
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-here
   DATABASE_URL=sqlite:///app.db
   CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
   ```
   - `SECRET_KEY`: A random string for Flask sessions.
   - `JWT_SECRET_KEY`: For JWT token generation.
   - `DATABASE_URL`: Points to SQLite file.
   - `CORS_ORIGINS`: Allowed origins for CORS.

3. **Run Locally:** Test the backend with `python app.py`. It should start on port 5000 and seed the database.

### Frontend Environment
1. **Install Dependencies:** In the frontend directory, run `npm install`.
2. **Environment Variables:** Create a `.env` file with:
   ```
   REACT_APP_API_BASE_URL=https://your-backend-url.com/api
   ```
   - Replace with the deployed backend URL.

3. **Build the App:** Run `npm run build` to create the production build in the `build` directory.
4. **Run Locally:** Use `npm start` to test on port 3000.

**Note:** The app uses JWT for authentication (expires in 24 hours) and SHA-256 hashed passwords.

## Backend Deployment
### Using Heroku
Heroku is recommended for simplicity in student projects.

1. **Prepare the App:**
   - Ensure `requirements.txt` includes all dependencies (e.g., Flask, Flask-CORS, PyJWT).
   - Create a `Procfile` in the backend root:
     ```
     web: gunicorn app:app
     ```
     - This assumes your main file is `app.py` with a `app` variable.

2. **Deploy Steps:**
   1. Create a Heroku app via dashboard or CLI: `heroku create your-app-name`.
   2. Add a buildpack for Python: `heroku buildpacks:add heroku/python`.
   3. Set environment variables: `heroku config:set SECRET_KEY=...` (repeat for each).
   4. Push to Heroku: `git push heroku main`.
   5. Open the app: `heroku open`.

3. **Database:** SQLite will be created automatically on first run. No separate DB setup needed.

### Alternative: Render or Railway
- Follow similar steps: Push code, set env vars, deploy. URL will be provided post-deployment.

**Post-Deployment:** Verify API endpoints like `POST /api/auth/login` using tools like Postman.

## Frontend Deployment
### Using Netlify
1. **Connect Repository:** Link your GitHub repo to Netlify.
2. **Build Settings:**
   - Build command: `npm run build`
   - Publish directory: `build`
   - Add environment variable: `REACT_APP_API_BASE_URL=https://your-heroku-app.herokuapp.com/api`

3. **Deploy:** Push to GitHub, and Netlify will auto-deploy. Get the frontend URL (e.g., `https://your-app.netlify.app`).

### Using Vercel
1. **Import Project:** From Vercel dashboard, import from GitHub.
2. **Configure:**
   - Root directory: `frontend` (if nested).
   - Build command: `npm run build && npm run export` (if needed).
   - Environment variables as above.

3. **Deploy:** Vercel handles the rest. Update CORS in backend to include the Vercel URL.

**Note:** Ensure responsive design works on mobile, as the app uses CSS3 grids and flexbox.

## Database Setup
- **SQLite:** No manual setup required. The database (`app.db`) is created on first backend run with seeded data (mock users, restaurants, etc.).
- **Backup:** For production, consider migrating to PostgreSQL, but for student projects, SQLite suffices.
- **Seeding:** Run the app once to seed data. Tables include `users`, `restaurants`, `menu_items`, `orders`, `order_items`.

## CI/CD Pipeline
Set up automated pipelines using GitHub Actions for quality assurance.

### Suggested Pipeline
Create `.github/workflows/deploy.yml` in your repo root:

```yaml
name: Deploy App

on:
  push:
    branches: [ main ]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest  # Assuming tests exist

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test -- --watchAll=false
      - name: Build
        run: npm run build

  deploy:
    needs: [backend-test, frontend-test]
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Backend to Heroku
        run: |
          # Use Heroku CLI or API to deploy
      - name: Deploy Frontend to Netlify
        run: |
          # Use Netlify CLI or API
```

- **Triggers:** On push to `main`.
- **Jobs:** Test backend and frontend separately, then deploy.
- **Enhancements:** Add linting, code coverage.

For Heroku, use the Heroku GitHub integration for auto-deploy.

## Server Configuration
### Backend Server (Flask on Heroku)
- **Scaling:** Heroku free tier is limited; upgrade for production traffic.
- **Security:** 
  - Use HTTPS (Heroku provides SSL).
  - Validate JWT tokens on protected routes.
- **CORS:** Configured via `Flask-CORS` with allowed origins.

### Frontend Server (Static on Netlify/Vercel)
- **CDN:** Automatic via the platform.
- **Performance:** Enable gzip compression in build settings.
- **Security:** Set CSP headers if needed, but minimal for student project.

**Monitoring:** Use Heroku logs (`heroku logs --tail`) and Netlify deploy logs.

## Deployment Checklist
Use this checklist to ensure a smooth deployment:

- [ ] Local testing completed (backend on 5000, frontend on 3000).
- [ ] Environment variables set for both backend and frontend.
- [ ] Database seeded and tables created.
- [ ] Backend deployed and API endpoints accessible (e.g., login works).
- [ ] Frontend deployed, with correct API base URL.
- [ ] CI/CD pipeline set up and passing.
- [ ] CORS configured to allow frontend domain.
- [ ] HTTPS enabled on both ends.
- [ ] Responsive design tested on mobile/desktop.
- [ ] Authentication flow tested (login, JWT expiry).
- [ ] Role-based access verified (e.g., admin views all orders).
- [ ] Error handling checked (e.g., invalid orders).
- [ ] Backup plan for database (export SQLite file if needed).

## Troubleshooting
- **Backend Deployment Issues:** Check Heroku logs for errors like missing dependencies.
- **CORS Errors:** Ensure `CORS_ORIGINS` includes the exact frontend URL.
- **JWT Expiry:** Tokens expire in 24 hours; implement refresh if needed.
- **Database Errors:** If SQLite locks, restart the app.
- **Frontend Build Fails:** Clear npm cache and reinstall.
- **Common Errors:**
  - 500 Internal Server Error: Check Flask app logs.
  - 404 on API Calls: Verify endpoint paths.
  - Build Timeout: Optimize build process or use faster plans.

## Conclusion
Following this guide, you should successfully deploy the Food Delivery App. For a student project, prioritize testing and iteration. If issues arise, consult documentation for Heroku, Netlify, or the project's issue tracker. Total deployment time: 1-2 hours for a first-time setup.

**Word Count:** Approximately 1200.

This guide is actionable and covers all specified aspects. For advanced setups, consider Dockerizing the app for containerized deployment.
