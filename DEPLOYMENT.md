# Publish Prep Track (Render + Vercel)

This repository is prepared for a Render FastAPI service and a Vercel Vite frontend. A live deployment still requires your hosting accounts and their project-specific URLs/secrets.

## 1. Push the project to GitHub

Create a new GitHub repository, then from this project folder run:

```bash
git init
git add .
git commit -m "Prepare Prep Track for production"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/prep-track.git
git push -u origin main
```

## 2. Deploy API + PostgreSQL on Render

- In Render, create a Blueprint from the GitHub repository and select `render.yaml`.
- Render creates a PostgreSQL database and the FastAPI web service.
- Set `FRONTEND_ORIGINS` on the API service to your exact Vercel URL (for example `https://prep-track.vercel.app`).
- Wait for the API service to become live. Test `https://YOUR-API.onrender.com/health` and `/docs`.

## 3. Deploy frontend on Vercel

- Import the same GitHub repository into Vercel.
- Set **Root Directory** to `frontend`.
- Framework preset: **Vite**; Build command: `npm run build`; Output directory: `dist`.
- Add environment variable `VITE_API_URL` with the Render API base URL, without a trailing slash.
- Deploy. The included `frontend/vercel.json` handles React Router routes.

## 4. Finish CORS and smoke tests

- Copy the final Vercel production URL into Render's `FRONTEND_ORIGINS` (comma-separated if you have more than one trusted origin), then redeploy the API.
- Test registration, sign in, adding/completing/deleting tasks, progress tracking, resources and sign out.
- Confirm that one test account cannot access another account's records.

## Production notes

- Keep `SECRET_KEY` private and use Render's generated value.
- Never commit `.env` files or database credentials.
- Back up the PostgreSQL database before major changes.
- SQLAlchemy currently creates tables at app startup. Add Alembic migrations before evolving production schemas.
- The free hosting tiers may sleep or have limits; check current provider pricing and policies before launch.
