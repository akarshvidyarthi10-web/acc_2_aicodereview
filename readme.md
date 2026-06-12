# AI Code Review Agent

This project is a full-stack AI Code Review Agent for GitHub Pull Requests. The backend handles GitHub webhooks, triggers AI review workflows, and posts comments to PRs. The frontend shows review status, issue summaries, and manual review actions.

## Project structure

- `backend/` - FastAPI backend service
- `frontend/` - React + Vite dashboard

## Backend structure

- `backend/main.py` - FastAPI entry point
- `backend/config/settings.py` - environment settings
- `backend/routes/` - webhook and review endpoints
- `backend/controllers/` - business logic handlers
- `backend/services/` - GitHub and AI integration
- `backend/models/` - data model definitions
- `backend/utils/` - reusable utilities
- `backend/schemas/` - request/response schemas
- `backend/.env.example` - example env variables

## Frontend structure

- `frontend/src/App.jsx` - app shell
- `frontend/src/pages/Dashboard.jsx` - dashboard page
- `frontend/src/components/` - reusable components
- `frontend/src/services/api.js` - backend API calls
- `frontend/src/hooks/useReviews.js` - review fetch hook

## Startup instructions

### Backend

1. `cd backend`
2. `python -m venv .venv`
3. `.
\.venv\Scripts\activate` (Windows)
4. `pip install -r requirements.txt`
5. create `.env` from `.env.example`
6. `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

### Frontend

1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Notes

- The backend currently includes placeholder AI logic in `backend/services/ai_service.py`.
- Replace the placeholder with AWS Bedrock integration when credentials are ready.
- GitHub webhook handling is in `backend/routes/webhook.py` and `backend/controllers/webhook_controller.py`.

