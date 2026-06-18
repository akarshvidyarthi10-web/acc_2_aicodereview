"""
Code Smell Agent: Identifies code quality issues and anti-patterns.
- Duplicate code
- Long methods/classes
- Magic numbers
- Dead code
- Complex conditions
- Poor naming patterns
"""
import json
from typing import TypedDict
from config.settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI


class SmellAgentOutput(TypedDict):
    smells: list


async def smell_agent(diff: str, review_context: dict = None) -> SmellAgentOutput:
    """Analyze code for code smells and anti-patterns."""
    
    prompt = f"""You are a code quality reviewer. Analyze this GitHub PR diff for code smells and anti-patterns.

Return ONLY a JSON object (no other text) with this structure:
{{
  "smells": [
    {{
      "severity": "HIGH|MEDIUM|LOW",
      "file": "filename.ext",
      "line": 15,
      "issue": "Description of the code smell",
      "suggestion": "How to improve this"
    }}
  ]
}}

Focus on:
- Duplicate code blocks
- Overly long methods (>20 lines)
- Large classes (>300 lines)
- Magic numbers without constants
- Dead/unreachable code
- Too many nested conditions
- Missing error handling
- Inconsistent naming
- Functions with too many parameters (>4)
- Comments indicating bad code ("TODO", "FIXME", "HACK")

Diff:
{diff}

Return ONLY valid JSON, nothing else."""

    try:
        print("Running Code Smell Agent...")
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
                result = {"smells": []}
        
        return SmellAgentOutput(smells=result.get("smells", []))
    
    except Exception as e:
        print(f"Smell agent error: {e}")
        return SmellAgentOutput(smells=[])
