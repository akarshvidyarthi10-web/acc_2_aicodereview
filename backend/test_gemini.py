import os
from config.settings import settings

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError as exc:
    raise SystemExit("Missing langchain_google_genai package. Run pip install -r requirements.txt") from exc

if not settings.gemini_api_key:
    raise SystemExit("GEMINI_API_KEY is not set in the environment.")

llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model or "gemini-2.5-flash",
    api_key=settings.gemini_api_key,
    temperature=0,
)

prompt = "Review this code:\n\n```python\nprint(\"Hello world\")\n```"
print('Sending prompt to Gemini...')
response = llm.invoke(prompt)
print('Response:')
print(response)
