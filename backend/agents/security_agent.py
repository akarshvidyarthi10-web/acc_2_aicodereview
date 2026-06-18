"""
Security Agent: Identifies security vulnerabilities and risky patterns.
- Hardcoded secrets/passwords
- SQL injection risks
- Command injection
- Unsafe cryptography
- Authentication/authorization issues
"""
import json
import time
from typing import TypedDict
from config.settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI


class SecurityAgentOutput(TypedDict):
    security: list


async def security_agent(diff: str, review_context: dict = None) -> SecurityAgentOutput:
    """Analyze code for security issues."""
    
    prompt = f"""You are a security code reviewer. Analyze this GitHub PR diff for security vulnerabilities.

Return ONLY a JSON object (no other text) with this structure:
{{
  "security": [
    {{
      "severity": "HIGH|MEDIUM|LOW",
      "file": "filename.ext",
      "line": 10,
      "issue": "Description of the vulnerability",
      "suggestion": "How to fix this"
    }}
  ]
}}

Focus on:
- Hardcoded secrets, passwords, API keys
- SQL injection, command injection
- Unsafe cryptography
- Authentication/authorization flaws
- Insecure deserialization
- Path traversal vulnerabilities
- Cross-site scripting (XSS)
- Insecure random number generation

Diff:
{diff}

Return ONLY valid JSON, nothing else."""

    try:
        print("Running Security Agent...")
        model_name = settings.gemini_model or settings.gemini_model_fallback or "gemini-1.5-flash"
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            api_key=settings.gemini_api_key,
            temperature=0,
        )

        response = llm.invoke(prompt)
        content = response if isinstance(response, str) else getattr(response, "content", str(response))
        
        # Extract JSON from response
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                result = json.loads(content[start:end])
            else:
                result = {"security": []}
        
        return SecurityAgentOutput(security=result.get("security", []))
    
    except Exception as e:
        print(f"Security agent error: {e}")
        return SecurityAgentOutput(security=[])
