import openai

import openai

class LLMReviewer:
    def __init__(self, api_key):
        openai.api_key = api_key

    def review_code(self, code_content, diagnostics):
        prompt = f"""
You are an expert Python code reviewer. Given the code and static analysis output,
provide concise, actionable feedback.

Code:
{code_content}

Static Analysis:
{diagnostics}

Respond with bullet points.
"""
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # going to use this model for now, going to change in the future
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message["content"]