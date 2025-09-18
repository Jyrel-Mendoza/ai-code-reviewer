from openai import OpenAI, OpenAIError, RateLimitError
from dotenv import load_dotenv
from pathlib import Path
import os


# Resolve path to utils/.env
env_path = Path(__file__).resolve().parent.parent / "utils" / ".env"
load_dotenv(dotenv_path=env_path)
print("Loaded key:", os.getenv("OPENAI_API_KEY"))

# Mock is in my .env file!
class OpenAIReviewer:
    def __init__(self, api_key=None):
        self.mock = os.getenv("MOCK_LLM", "false").lower() == "true"
        if not self.mock:
            self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def review(self, code_content, diagnostics):
        if self.mock:
            # Fake response for testing
            return f"🔧 Mock feedback: Found {len(code_content.splitlines())} lines of code and {len(diagnostics)} diagnostics."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            return response.choices[0].message.content

        except RateLimitError:
            return "❌ Rate limit or quota exceeded. Please check your OpenAI plan/billing."
        except OpenAIError as e:
            return f"❌ OpenAI API error: {str(e)}"