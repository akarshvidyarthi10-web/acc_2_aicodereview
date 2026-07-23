"""
Naming Agent: Reviews naming conventions and readability.
- Variable names clarity
- Function/method naming
- Class naming
- Constant naming
- Parameter naming
"""
import json
from typing import TypedDict
from config.settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI


class NamingAgentOutput(TypedDict):
    naming: list


async def naming_agent(diff: str, review_context: dict = None) -> NamingAgentOutput:
    """Analyze code for naming issues and readability."""
    
    prompt = f"""You are a naming conventions reviewer. Analyze this GitHub PR diff for naming issues.

Return ONLY a JSON object (no other text) with this structure:
{{
  "naming": [
    {{
      "severity": "MEDIUM|LOW",
      "file": "filename.ext",
      "line": 20,
      "issue": "Description of naming problem",
      "suggestion": "Suggested better name"
    }}
  ]
}}

Focus on:
- Single letter variable names (except i, j in loops)
- Abbreviations that reduce clarity
- Inconsistent naming style (camelCase vs snake_case)
- Variables that don't describe their purpose
- Non-English names
- Names that don't match their usage
- Class names that are too generic
- Function names that don't describe what they do
- Confusing or misleading names

Diff:
{diff}

Return ONLY valid JSON, nothing else."""

    try:
        print("Running Naming Agent...")
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
                result = {"naming": []}
        
        return NamingAgentOutput(naming=result.get("naming", []))
    
    except Exception as e:
        print(f"Naming agent error: {e}")
        return NamingAgentOutput(naming=[])
