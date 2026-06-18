Checking the backend storage flow and webhook form fields so I can give the exact values and add MongoDB support cleanly.

Searched for regex `fetch_review_list|execute_manual_review|placeholder|MongoDB|db\.|motor|pymongo` (`**/backend/**`), 13 results

I found the placeholder review storage path. Next I’ll add MongoDB support and give the webhook form values.

Read [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/services/analysis_service.py)

Read [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/config/settings.py)

Adding MongoDB storage integration and updating backend config/requirements to support it.

Created [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/services/db_service.py)

Replacing 44 lines with 52 lines in [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/config/settings.py), [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/services/analysis_service.py), [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/requirements.txt)


```

```

```

```

```

```


Read [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/.env.example)

Replacing 5 lines with 6 lines in [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/.env.example)


```

```


Read [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/routes/webhook.py)

I’m wiring webhook secret verification so the GitHub form secret is actually used by the backend.

Created [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/utils/github_webhook.py)

Replacing 13 lines with 17 lines in [](file:///c%3A/Users/akarsh.vidyarthi/OneDrive%20-%20Accenture/Desktop/accenture_project%202/backend/routes/webhook.py)


```

```
## ✅ Storage choice

Yes — use **MongoDB** for review storage.

- I added `MONGODB_URI` support in settings.py
- Backend now uses `motor` and db_service.py
- Example in .env.example:
  - `MONGODB_URI=mongodb://localhost:27017`

So your database config becomes:
- `backend/.env`
  - `GITHUB_TOKEN=...`
  - `GITHUB_WEBHOOK_SECRET=...`
  - `GEMINI_API_KEY=...`
  - `GEMINI_MODEL=gemini-2.5-flash`
  - `MONGODB_URI=mongodb://localhost:27017`

---

## 🔧 GitHub webhook form values

Fill the webhook form like this:

- **Payload URL**
  - `https://<your-public-domain>/api/webhook`
  - Example: `https://abc123.ngrok.app/api/webhook` if using ngrok locally
  - Or production: `https://your-app.com/api/webhook`

- **Content type**
  - `application/json`

- **Secret**
  - Use the same secret value as `GITHUB_WEBHOOK_SECRET` in your backend `.env`
  - Example: `my_super_secret_value`

- **SSL verification**
  - Keep it enabled if your URL is HTTPS
  - If using ngrok or proper TLS, use **Enable SSL verification**

- **Which events**
  - Best choice: `Let me select individual events`
  - Select **Pull requests**
  - If you want broader coverage, you can also add **Push** later, but PR open/edited is enough for this design

- **Active**
  - Keep it checked

---

## 📌 Important note

I also added webhook security support in webhook.py:
- verifies `X-Hub-Signature-256`
- compares it against `GITHUB_WEBHOOK_SECRET`

So the secret is actually enforced by the backend now.

If you want, I can also add support for GitHub webhook `pull_request` action filtering to only run on `opened`, `synchronize`, and `reopened`.

Made changes.