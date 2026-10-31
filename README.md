# Prep Track

A full-stack placement preparation workspace built with React, Vite, FastAPI, SQLAlchemy and PostgreSQL (SQLite is used by default for local development).

## Features
- Account registration, login and JWT-protected personal workspace
- Dashboard with live preparation statistics
- Create, complete and delete preparation tasks
- Track solved questions by topic
- Save and manage learning resources
- Responsive UI for desktop and mobile
- PostgreSQL in production; SQLite for local development

## Run locally

### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

### Frontend (new terminal)
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Open http://localhost:5173.

## Deploy
1. Create a managed PostgreSQL database and copy its connection URL.
2. Deploy `backend/` as a Python web service. Build/install command: `pip install -r requirements.txt`; start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
3. Set backend environment variables: `DATABASE_URL` (PostgreSQL URL), `SECRET_KEY` (long random secret), and `FRONTEND_ORIGINS` (your deployed frontend origin).
4. Deploy `frontend/` as a Vite static site. Build command: `npm run build`; output directory: `dist`. Set `VITE_API_URL` to the deployed backend URL.
5. Redeploy the frontend after setting `VITE_API_URL`; test registration, login, tasks, progress and resources on the live domain.

The included `frontend/vercel.json` supports client-side route fallback. Do not commit real `.env` files or production secrets. For a production launch with important user data, add Alembic migrations, automated backups, rate limiting and email verification before broad public use.
