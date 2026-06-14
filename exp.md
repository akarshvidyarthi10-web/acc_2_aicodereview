# AI Code Review Agent - Project Explanation

## 1. Project Overview
यह प्रोजेक्ट एक AI Code Review Agent है जो GitHub Pull Requests को review करने के लिए बनाया गया है।

- Backend: FastAPI service जो GitHub webhook process करती है, PR diff लेती है, AI review बनाती है, MongoDB में save करती है, और comment GitHub PR पर post करती है।
- Frontend: React + Vite dashboard जो saved reviews दिखाती है और review status track करती है।

## 2. अभी तक क्या बनाया गया है

### Backend

#### `backend/main.py`
- FastAPI एप्लीकेशन का entry point है।
- CORS middleware जोड़ता है ताकि frontend local server से backend को access कर सके।
- दो router include करता है: `webhook` और `review`।
- `/` और `/health` endpoints provide करता है जो service status बताता है।

#### `backend/config/settings.py`
- Pydantic `BaseSettings` इस्तेमाल करके environment variables load करता है।
- GitHub token, Bedrock model, webhook secret, MongoDB URI आदि configure करता है।
- `.env` file से settings लेता है।

#### `backend/routes/webhook.py`
- GitHub webhook receiver endpoint है: `POST /api/webhook`।
- GitHub signature verify करता है `utils/github_webhook.py` से।
- valid payload मिलने पर `controllers/webhook_controller.handle_webhook` को delegate करता है।

#### `backend/routes/review.py`
- Review related endpoints expose करता है:
  - `GET /api/reviews` → सभी reviews list
  - `GET /api/reviews/{review_id}` → review details
  - `POST /api/reviews/run` → manual review trigger

#### `backend/controllers/webhook_controller.py`
- webhook payload process करता है, केवल `opened`, `synchronize`, `reopened` actions handle करता है।
- PR details से repo और PR नंबर लेता है।
- `services/github_service.get_pr_files` से PR की changed files fetch करता है।
- file patch को जोड़कर code diff बनाता है।
- `services.ai_service.analyze_code` को diff देता है जिससे AI review result मिलता है।
- review result MongoDB में `services.db_service.save_review` से save करता है।
- GitHub PR पर comment post करता है `services.github_service.post_comment` के जरिए।

#### `backend/controllers/review_controller.py`
- frontend या manual review calls को backend service layer से connect करता है।
- review list, detail, और manual review request को appropriate service functions तक पहुंचाता है।

#### `backend/services/github_service.py`
- GitHub REST API calls करता है।
- `get_pr_files`: PR files डेटा fetch करने के लिए GitHub `/pulls/{pr_number}/files` endpoint।
- `post_comment`: PR issue comment बनाकर GitHub पर भेजता है।
- `httpx.AsyncClient` का उपयोग async HTTP requests के लिए किया गया है।

#### `backend/services/ai_service.py`
- अबhi placeholder AI review generate करता है।
- `analysis` के लिए diff से prompt बनाता है और review structure return करता है।
- real Bedrock या AI integration अभी TODO है। इसलिए यह placeholder comment और response return करता है।
- `utils/formatter.format_review` से markdown review comment format किया जाता है।

#### `backend/services/db_service.py`
- MongoDB से connect करता है `motor.motor_asyncio.AsyncIOMotorClient` के साथ।
- `list_reviews`: सभी reviews लाता है।
- `get_review_by_id`: एक review search करता है।
- `save_review`: review data में UUID id और timestamp जोड़कर insert करता है।

#### `backend/services/analysis_service.py`
- review list/detail के backend logic को संभालता है।
- `execute_manual_review`: manual review request को queue करने का stub बनाता है।
- यह अभी सिर्फ placeholder response बनाता है।

#### `backend/utils/formatter.py`
- review result को markdown comment में format करता है।
- Summary, Issues, Suggestions को readable text में बदलता है।
- GitHub comment body बनाने के लिए उपयोगी है।

#### `backend/utils/github_webhook.py`
- GitHub webhook secret के साथ HMAC-SHA256 signature verify करता है।
- यह सुरक्षा के लिए जरूरी है ताकि केवल GitHub से आए webhook स्वीकार हों।

#### `backend/utils/logger.py`
- simple logging setup करता है।
- logs को console पर print करता है ताकि debugging आसान हो।

### Frontend

#### `frontend/src/App.jsx`
- React app का root component है।
- `Dashboard` component render करता है।

#### `frontend/src/pages/Dashboard.jsx`
- main dashboard page है।
- `useReviews` hook से reviews fetch करता है।
- loading, error state handle करता है और `PRList` component को data pass करता है।

#### `frontend/src/hooks/useReviews.js`
- React hook है जो backend API से review data लेता है।
- `fetchReviews` function बनाता है।
- state manage करता है: `reviews`, `loading`, `error`।

#### `frontend/src/services/api.js`
- backend API URL configure करता है।
- `getReviews()` और `getReview(id)` functions define करता है।
- fetch response check करता है और JSON return करता है।

#### `frontend/src/components/PRList.jsx`
- review list render करता है।
- अगर कोई PR review नहीं है तो fallback message देता है।
- प्रत्येक review के लिए `ReviewCard` बनाता है।

#### `frontend/src/components/ReviewCard.jsx`
- एक single review summary card दिखाता है।
- review title, status, issues count show करता है।

## 3. क्यों ये चीजें उपयोग की गई हैं

- FastAPI: backend API बनाने के लिए, async support और automatic docs के लिए।
- httpx: async HTTP requests करने के लिए, GitHub API calls के लिए।
- motor: async MongoDB driver, ताकि database operations non-blocking हों।
- Pydantic settings: environment variables safe तरीके से पढ़ने के लिए।
- React + Vite: frontend UI बनाने के लिए modern JavaScript framework।
- HMAC-SHA256 verification: GitHub webhook security के लिए जरूरी।
- Markdown formatting: GitHub comment readable output देने के लिए।

## 4. अब तक क्या काम कर रहा है

- GitHub webhook receive होता है।
- webhook signature verify होता है।
- PR files fetch होती हैं और diff बनता है।
- placeholder AI review generate होता है।
- review MongoDB में save होता है।
- GitHub PR पर comment पोस्ट होता है।
- frontend dashboard review list display करता है।

## 5. क्या पूरा नहीं हुआ / आगे क्या करना है

### जरूरी काम

1. AI integration पूरी करना
   - `backend/services/ai_service.py` में placeholder को replace करना
   - AWS Bedrock, OpenAI, या कोई मॉडल service integrate करना
   - diff analysis को real `summary`, `issues`, `suggestions` देना

2. GitHub review flow improve करना
   - PR comments को better structure देना
   - `pull_request.review_comments` या `reviews` endpoint से deeper integration
   - error handling और retry logic जोड़ना

3. Frontend features बढ़ाना
   - detailed review page (`ReviewDetails.jsx`) बनाना
   - manual review trigger UI जो `POST /api/reviews/run` call करे
   - review issue list और suggestions render करना
   - better styling and responsive layout

4. Database और data modeling
   - review schema validate करना
   - unique PR cache/replace logic जोड़ना (duplicate insert रोकना)
   - created_at, updated_at, status transitions manage करना

5. Deployment and env setup
   - `.env.example` / real `.env` configure करना
   - production deployment plan बनाना (Docker, cloud, ngrok या hosted service)
   - health checks, logging, monitoring जोड़ना

6. Tests
   - backend unit tests और API tests
   - frontend component tests
   - webhook signature और GitHub API mocks

## 6. फाइलों का सारांश

- `backend/main.py`: app startup
- `backend/config/settings.py`: config loader
- `backend/routes/webhook.py`: webhook receive endpoint
- `backend/routes/review.py`: review-related API endpoints
- `backend/controllers/webhook_controller.py`: webhook process logic
- `backend/controllers/review_controller.py`: review controller layer
- `backend/services/github_service.py`: GitHub REST API calls
- `backend/services/ai_service.py`: code analysis logic (placeholder)
- `backend/services/db_service.py`: MongoDB persistence
- `backend/services/analysis_service.py`: review list/detail/manual review logic
- `backend/utils/formatter.py`: review markdown builder
- `backend/utils/github_webhook.py`: webhook signature verification
- `backend/utils/logger.py`: logging setup
- `frontend/src/App.jsx`: React app root
- `frontend/src/pages/Dashboard.jsx`: main dashboard page
- `frontend/src/hooks/useReviews.js`: API data hook
- `frontend/src/services/api.js`: backend API client
- `frontend/src/components/PRList.jsx`: review list renderer
- `frontend/src/components/ReviewCard.jsx`: review card UI

## 7. Goal and Research Plan (Hinglish)

Our goal is to make this internship project into an **AI Code Review Agent** that behaves like a senior developer.

- Ye agent automatically Pull Requests review karega.
- Code smells, security vulnerabilities, naming convention violations, aur code quality issues identify karega.
- Saath hi improvement suggestions bhi dega, jaise ek senior dev code review karta hai.
- Aur agent direct GitHub PR par review comments post kar sake.

### Research aur preparation kya honi chahiye

1. Technology stack decide karo:
   - Backend: FastAPI + Python
   - Frontend: React + Vite
   - Database: MongoDB
   - AI model: AWS Bedrock, OpenAI, ya koi aur LLM service
   - GitHub integration: GitHub REST API, webhooks, comments/reviews endpoint

2. Problem areas samjho:
   - Code smell detection: duplicate code, long methods, complex logic
   - Security issues: SQL injection, insecure config, weak auth patterns
   - Naming conventions: variable, function, class names consistency
   - Best practices: error handling, logging, clean architecture

3. Architecture design socho:
   - Webhook receiver → PR diff fetch → AI analysis → result format → DB save → GitHub comment
   - Dashboard for review status, issues summary, manual rerun
   - Async flow for webhook processing and API responses

4. Proposed solutions:
   - AI model prompt design: diff aur context input, output mein summary/issues/suggestions
   - Review formatting: Markdown comment with sections and numbered issues
   - Feedback loop: manual review request, retry on failure, review history

5. Team discussion mein laane layak points:
   - Kaunse AI provider use karenge aur kyun
   - Webhook security kis tarah ensure karenge
   - Kaunsa data DB mein store karna hai (PR metadata, AI result, status)
   - Frontend UX: kis tarah review cards aur detail view honge

### Aage kya kya karna hai

1. `backend/services/ai_service.py` me real AI integration add karna.
2. GitHub PR comment logic ko actual review comment style me improve karna.
3. `frontend` me detailed review page aur manual trigger add karna.
4. Review data model ko strong banane ke liye schema validation aur status handling.
5. Testing aur deployment plan ready karna.

## 8. निष्कर्ष
यह प्रोजेक्ट एक अच्छी शुरुआत है। backend ने webhook, GitHub integration, database persistence, और review pipeline structure तैयार किया है। frontend ने dashboard और review list view provide किया है।

अगला मुख्य काम AI analysis को असली बनाना, GitHub review flow को complete करना, और frontend में detailed review experience जोड़ना है।