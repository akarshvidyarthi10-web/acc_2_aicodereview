# AI Code Review Agent

This project is a full-stack AI Code Review Agent for GitHub Pull Requests. The backend handles GitHub webhooks, triggers AI review workflows, and posts comments to PRs. The frontend shows review status, issue summaries, and manual review actions.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (local or Docker)
- GitHub repository + personal access token
- ngrok (for local webhook testing)

### 1️⃣ Setup Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

Create `backend/.env`:
```
GITHUB_TOKEN=your_github_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
MONGODB_URI=mongodb://localhost:27017
```

Start MongoDB:
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

Run backend:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs

### 2️⃣ Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:4173

### 3️⃣ Setup GitHub Webhook

Start ngrok:
```bash
ngrok http 8000
```

Get the URL (e.g., `https://abc123.ngrok.app`)

In your GitHub repo → Settings → Webhooks → Add webhook:
- **Payload URL:** `https://abc123.ngrok.app/api/webhook`
- **Content type:** `application/json`
- **Secret:** (same as `GITHUB_WEBHOOK_SECRET` in `.env`)
- **Events:** Pull requests
- **SSL verification:** Enable
- **Active:** ✅

Create a test PR — backend should log the webhook and post a review!

---

## 📁 Project Structure

- `backend/` - FastAPI service
  - `main.py` - entry point
  - `config/settings.py` - environment config
  - `routes/` - webhook + review endpoints
  - `controllers/` - business logic
  - `services/` - GitHub + AI + database
  - `utils/` - helpers + logging

- `frontend/` - React + Vite dashboard
  - `src/pages/Dashboard.jsx` - main view
  - `src/components/` - reusable UI
  - `src/services/api.js` - backend calls
  - `src/hooks/useReviews.js` - data fetching

---

## 📖 Full Setup Guide

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions.

---

## 🔗 API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `POST /api/webhook` - GitHub webhook receiver
- `GET /api/reviews` - List all reviews
- `GET /api/reviews/{id}` - Review details
- `POST /api/reviews/run` - Trigger manual review

---

## 🔑 Environment Variables

See `backend/.env.example` for all options.

---

## 📝 Notes

- Gemini integration is configured in `backend/services/ai_service.py`
- MongoDB stores reviews in `ai_code_review.reviews` collection
- GitHub webhook signature verified with `GITHUB_WEBHOOK_SECRET`

