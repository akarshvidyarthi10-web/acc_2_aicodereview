import asyncio
from datetime import datetime, timedelta
from services.db_service import save_review, db

DUMMY_REVIEWS = [
    {
        "repository": "gh-user/repo-frontend",
        "pr_number": 12,
        "title": "Fix sign-in bug on login form",
        "summary": "The AI review found insecure password handling and outdated dependency usage.",
        "status": "completed",
        "security": [
            {
                "issue": "Hard-coded credentials found in authentication logic.",
                "severity": "HIGH",
                "file": "src/components/LoginForm.jsx",
                "line": 43,
                "suggestion": "Move credentials into environment variables and use secure storage.",
            }
        ],
        "smells": [
            {
                "issue": "Legacy validation pattern with nested callbacks.",
                "severity": "MEDIUM",
                "file": "src/components/LoginForm.jsx",
                "line": 21,
                "suggestion": "Refactor validation into reusable hooks or schema-based validation.",
            }
        ],
        "naming": [
            {
                "issue": "Variable name 'dataObj' is too generic.",
                "severity": "LOW",
                "file": "src/components/LoginForm.jsx",
                "line": 18,
                "suggestion": "Rename to 'loginPayload' or 'credentialsData'.",
            }
        ],
        "suggestions": [
            {
                "issue": "Use HTTPS-only cookies for auth tokens.",
                "severity": "LOW",
            }
        ],
        "security_issues": [
            {
                "issue": "Hard-coded credentials found in authentication logic.",
                "severity": "HIGH",
                "file": "src/components/LoginForm.jsx",
                "line": 43,
                "suggestion": "Move credentials into environment variables and use secure storage.",
            }
        ],
        "code_smells": [
            {
                "issue": "Legacy validation pattern with nested callbacks.",
                "severity": "MEDIUM",
                "file": "src/components/LoginForm.jsx",
                "line": 21,
                "suggestion": "Refactor validation into reusable hooks or schema-based validation.",
            }
        ],
        "best_practice_suggestions": [
            {
                "issue": "Use HTTPS-only cookies for auth tokens.",
                "severity": "LOW",
            }
        ],
        "review_score": 64,
        "recommendation": "REQUEST_CHANGES",
        "model": "gemini-2.5-flash",
        "processing_time": "2.74s",
        "created_at": (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z",
    },
    {
        "repository": "gh-user/repo-backend",
        "pr_number": 28,
        "title": "Improve database query handling",
        "summary": "The AI review found performance issues in the query builder and missing error handling.",
        "status": "completed",
        "security": [
            {
                "issue": "Potential SQL injection-like string concatenation in query builder.",
                "severity": "HIGH",
                "file": "backend/db.py",
                "line": 58,
                "suggestion": "Use parameterized queries or ORM query builders.",
            }
        ],
        "smells": [
            {
                "issue": "Duplicated error handling across DB methods.",
                "severity": "MEDIUM",
                "file": "backend/db.py",
                "line": 31,
                "suggestion": "Extract common error handling into a helper function.",
            }
        ],
        "naming": [],
        "suggestions": [
            {
                "issue": "Add retries for transient database failures.",
                "severity": "LOW",
            }
        ],
        "security_issues": [
            {
                "issue": "Potential SQL injection-like string concatenation in query builder.",
                "severity": "HIGH",
                "file": "backend/db.py",
                "line": 58,
                "suggestion": "Use parameterized queries or ORM query builders.",
            }
        ],
        "code_smells": [
            {
                "issue": "Duplicated error handling across DB methods.",
                "severity": "MEDIUM",
                "file": "backend/db.py",
                "line": 31,
                "suggestion": "Extract common error handling into a helper function.",
            }
        ],
        "best_practice_suggestions": [
            {
                "issue": "Add retries for transient database failures.",
                "severity": "LOW",
            }
        ],
        "review_score": 70,
        "recommendation": "REQUEST_CHANGES",
        "model": "gemini-2.5-flash",
        "processing_time": "2.10s",
        "created_at": (datetime.utcnow() - timedelta(days=2)).isoformat() + "Z",
    },
    {
        "repository": "gh-user/repo-frontend",
        "pr_number": 34,
        "title": "Refactor signup page styling",
        "summary": "The AI review found good structure, but recommended improving validation and consistency.",
        "status": "completed",
        "security": [],
        "smells": [
            {
                "issue": "Repeated style definitions in multiple components.",
                "severity": "LOW",
                "file": "src/pages/Signup.jsx",
                "line": 12,
                "suggestion": "Extract shared styles into a common component.",
            }
        ],
        "naming": [
            {
                "issue": "Function name 'handleSignUp' is fine but can be more specific.",
                "severity": "LOW",
                "file": "src/pages/Signup.jsx",
                "line": 14,
                "suggestion": "Rename to 'handleUserSignup' for clarity.",
            }
        ],
        "suggestions": [
            {
                "issue": "Ensure validation messages are accessible for screen readers.",
                "severity": "LOW",
            }
        ],
        "security_issues": [],
        "code_smells": [
            {
                "issue": "Repeated style definitions in multiple components.",
                "severity": "LOW",
                "file": "src/pages/Signup.jsx",
                "line": 12,
                "suggestion": "Extract shared styles into a common component.",
            }
        ],
        "best_practice_suggestions": [
            {
                "issue": "Ensure validation messages are accessible for screen readers.",
                "severity": "LOW",
            }
        ],
        "review_score": 70,
        "recommendation": "APPROVE",
        "model": "gemini-2.5-flash",
        "processing_time": "1.96s",
        "created_at": datetime.utcnow().isoformat() + "Z",
    },
]


async def seed():
    await db.reviews.delete_many({})
    for review in DUMMY_REVIEWS:
        saved = await save_review(review)
        print(f"Inserted review {saved['repository']} #{saved['pr_number']} id={saved['id']}")


if __name__ == '__main__':
    asyncio.run(seed())
