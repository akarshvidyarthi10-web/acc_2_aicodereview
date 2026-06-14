# 🚀 Complete Setup Guide

## 1️⃣ NGROK SETUP (for local webhook testing)

### Install ngrok
```bash
# Download from https://ngrok.com/download
# Or using chocolatey on Windows:
choco install ngrok
```

### Start ngrok tunnel
```bash
ngrok http 8000
```

This gives you a URL like:
```
https://abc123def456.ngrok.app
```

**Copy this URL** — you'll use it for the GitHub webhook.

---

## 2️⃣ BACKEND SETUP

### 1. Create `.env` file in `backend/` folder

```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_WEBHOOK_SECRET=my_super_secret_webhook_key_12345
BEDROCK_MODEL=amazon.titan
BEDROCK_REGION=us-east-1
MONGODB_URI=mongodb://localhost:27017
```

**Get GITHUB_TOKEN:**
- Go to https://github.com/settings/tokens
- Create a new "Fine-grained personal access token"
- Permissions needed:
  - Repository > Pull requests (read)
  - Repository > Issues (read + write) — for posting comments

**GITHUB_WEBHOOK_SECRET:**
- Use any random string (example: `webhook_secret_12345`)
- Keep it safe — you'll need it for GitHub webhook form too

### 2. Install dependencies

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 3. Start MongoDB (if not running)

```bash
# Using Docker:
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or if MongoDB installed locally:
mongod
```

### 4. Run FastAPI backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Output should show:**
```
Uvicorn running on http://0.0.0.0:8000
```

---

## 3️⃣ FRONTEND SETUP

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Run Vite dev server

```bash
npm run dev
```

**Output should show:**
```
Local:   http://localhost:4173/
```

---

## 4️⃣ GITHUB WEBHOOK CONFIGURATION

### Go to GitHub webhook settings

1. Navigate to your repository: https://github.com/akarshvidyarthi10-web/acc_2_aicodereview
2. Click **Settings** → **Webhooks** → **Add webhook**

### Fill the form with:

- **Payload URL:** `https://abc123def456.ngrok.app/api/webhook`
  - Replace `abc123def456` with your actual ngrok URL from step 1️⃣

- **Content type:** `application/json`

- **Secret:** `my_super_secret_webhook_key_12345`
  - Use the SAME value as `GITHUB_WEBHOOK_SECRET` in your `.env`

- **SSL verification:** ✅ Enable SSL verification

- **Which events:**
  - Select: **Let me select individual events**
  - Check only: ✅ **Pull requests**
  - (Optionally add **Pushes** if you want to review commits too)

- **Active:** ✅ Check this box

- Click **Add webhook**

---

## 5️⃣ TEST THE WORKFLOW

### 1. Create a test PR

```bash
# In your repo, create a new branch:
git checkout -b test/webhook-test
echo "// test code" > test.js
git add test.js
git commit -m "test PR"
git push origin test/webhook-test
```

Then open a Pull Request on GitHub.

### 2. Check logs

**Backend terminal** should show:
```
POST /api/webhook - "GitHub webhook received"
```

**MongoDB** should have a new review document in `reviews` collection.

**GitHub PR** should get an auto-comment with the AI review (once Bedrock is wired).

---

## ⚙️ Environment Variables Summary

### Backend (.env)

```
GITHUB_TOKEN=ghp_xxxxx              # GitHub personal access token
GITHUB_WEBHOOK_SECRET=webhook_xxx   # Secret for webhook verification
BEDROCK_MODEL=amazon.titan          # AWS Bedrock model
BEDROCK_REGION=us-east-1            # AWS region
MONGODB_URI=mongodb://localhost:27017
```

### Frontend (.env or .env.local — optional)

```
VITE_API_URL=http://localhost:8000/api
```

---

## 🔍 Troubleshooting

### Webhook not triggering?
- Check ngrok URL is correct in GitHub webhook settings
- Check `GITHUB_WEBHOOK_SECRET` matches in both `.env` and GitHub webhook form
- Check backend is running: `http://localhost:8000/`

### MongoDB connection error?
- Ensure MongoDB is running on `localhost:27017`
- Or update `MONGODB_URI` in `.env` to your MongoDB connection string

### GitHub API errors?
- Check `GITHUB_TOKEN` has correct permissions
- Token should have **Pull requests (read)** and **Issues (read + write)**

---

## ✅ Next Steps (AFTER Bedrock is ready)

1. Update `backend/services/ai_service.py` with Bedrock integration
2. Test with a new PR — should get auto-comments with AI review
3. Frontend Dashboard will show reviews from MongoDB

