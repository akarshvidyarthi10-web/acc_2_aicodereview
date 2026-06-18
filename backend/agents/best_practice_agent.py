"""
Best Practice Agent: Reviews adherence to best practices and design patterns.
- SOLID principles
- DRY principle
- Error handling
- Testing considerations
- Documentation
- Type safety
"""
import json
from typing import TypedDict
from config.settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI


class BestPracticeAgentOutput(TypedDict):
    suggestions: list


async def best_practice_agent(diff: str, review_context: dict = None) -> BestPracticeAgentOutput:
    """Analyze code for best practice violations."""
    
    prompt = f"""You are a software engineering best practices reviewer. Analyze this GitHub PR diff for best practice issues.

Return ONLY a JSON object (no other text) with this structure:
{{
  "suggestions": [
    {{
      "severity": "MEDIUM|LOW",
      "file": "filename.ext",
      "line": 25,
      "issue": "Description of best practice violation",
      "suggestion": "Recommended improvement"
    }}
  ]
}}

Focus on:
- SOLID principles (Single responsibility, Open/closed, Liskov, Interface, Dependency)
- DRY principle (Don't repeat yourself)
- KISS principle (Keep it simple)
- Proper error handling
- Missing input validation
- Testability concerns
- Documentation and comments
- Type hints and type safety
- Resource management (file handles, connections)
- Performance considerations
- Logging appropriateness

Diff:
{diff}

Return ONLY valid JSON, nothing else."""

    try:
        print("Running Best Practice Agent...")
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
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                result = json.loads(content[start:end])
            else:
                result = {"suggestions": []}
        
        return BestPracticeAgentOutput(suggestions=result.get("suggestions", []))
    
    except Exception as e:
        print(f"Best practice agent error: {e}")
        return BestPracticeAgentOutput(suggestions=[])
