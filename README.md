# Student Performance Tracker — Backend

FastAPI backend powering the Student Performance Tracker: authentication, CRUD, data analytics, a machine learning prediction service, and a GenAI-powered tutor chatbot.

Live API: https://student-performance-tracker-backend-umpd.onrender.com
Interactive API docs (Swagger): https://student-performance-tracker-backend-umpd.onrender.com/docs

Note: the API is hosted on Render's free tier, which spins down after periods of inactivity. The first request after idle time may take 30-60 seconds to respond while the server wakes up.

## Features

- Authentication and Authorization: JWT-based auth with role-based access control (admin / teacher / student)
- Core CRUD: Students, courses, and grades, fully validated with Pydantic schemas
- Data Analytics: Aggregation endpoints for student averages, course performance, class pass rates, and score trends
- Machine Learning: A RandomForest regression model predicts a student's next likely score, and a RandomForest classifier flags at-risk students, both trained on a synthetic dataset and served live against real student data
- GenAI Tutor: A chatbot endpoint (powered by Groq's Llama 3.1) that answers natural-language questions about a specific student, grounded in their real grade history and ML predictions

## Tech Stack

- Framework: FastAPI
- Database: SQLite (dev) via SQLAlchemy ORM
- Auth: JWT (python-jose), bcrypt password hashing
- ML: scikit-learn, pandas, numpy
- GenAI: Groq API (Llama 3.1)
- Deployment: Render

## Project Structure

app/
- api/routers/ : Route handlers (auth, students, courses, grades, analytics, ml, tutor)
- core/ : Config and security utilities
- db/ : Database engine/session setup
- models/ : SQLAlchemy ORM models
- schemas/ : Pydantic request/response schemas
- ml/ : ML training pipeline, trained models, and GenAI tutor service
- main.py : App entrypoint

## Running Locally

1. Clone the repo and create a virtual environment:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Create a .env file:
   DATABASE_URL=sqlite:///./spt.db
   SECRET_KEY=your_random_secret_key
   GROQ_API_KEY=your_groq_api_key
   FRONTEND_ORIGIN=http://localhost:5173

3. Generate the ML models (one-time setup):
   python app/ml/generate_synthetic_data.py
   python app/ml/train_model.py

4. Run the server:
   uvicorn app.main:app --reload --port 8000

5. Visit http://localhost:8000/docs for the interactive API documentation.

## Key API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/auth/register | Create a new user account |
| POST | /api/v1/auth/login | Log in and receive a JWT |
| GET | /api/v1/students/ | List students |
| POST | /api/v1/grades/ | Record a new grade |
| GET | /api/v1/analytics/student-averages | Per-student score/attendance averages |
| GET | /api/v1/ml/predict/{student_id} | ML-predicted next score + at-risk flag |
| POST | /api/v1/tutor/{student_id} | Ask the GenAI tutor a question about a student |

## Related Repository

Frontend: https://github.com/Hardikpateriya2025/student-performance-tracker-frontend
