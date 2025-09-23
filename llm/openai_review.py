from openai import OpenAI, OpenAIError, RateLimitError
from dotenv import load_dotenv
from pathlib import Path
from utils.chunker import chunk_code
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

    def review(self, code_content, diagnostics, mode="style"):
        if self.mock:
            return f"🔧 Mock feedback: Found {len(code_content.splitlines())} lines of code and {len(diagnostics)} diagnostics."

        mode_instruction = MODE_PROMPTS.get(mode, "")
        all_feedback = []

        for chunk in chunk_code(code_content, max_lines=100):
            messages = [
                {"role": "system", "content": BASE_PROMPT + "\n" + mode_instruction},
                *FEW_SHOT_EXAMPLES,
                {
                    "role": "user",
                    "content": f"Code:\n{chunk}\n\nStatic Analysis:\n{diagnostics}",
                },
            ]

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0,
            )
            all_feedback.append(response.choices[0].message.content)

        return "\n---\n".join(all_feedback)

    def suggest_fixes(self, code_content, diagnostics):
        if self.mock:
            return f"🔧 Mock fixed code:\n{code_content}"

        all_chunks = []

        for chunk in chunk_code(code_content, max_lines=100):
            prompt = f"""
You are a Python code auto-fixer. Improve the following code based on diagnostics.
Only return valid Python code, no explanations.

Code:
{chunk}

Diagnostics:
{diagnostics}
"""
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )

            fixed_chunk = response.choices[0].message.content
            all_chunks.append(fixed_chunk.strip())

        # Reassemble fixed code
        return "\n".join(all_chunks)