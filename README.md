AI Code Reviewer - By Jyrel!!! 🧑‍💻🤖

This is a developer tool that combines static analysis (flake8, pylint + more to come!) with LLM-based natural language feedback to review Python code.
Supports single files, whole repositories, multiple review modes, and even AI-generated fixes.

✨ Features
🔍 Static Analysis: Runs flake8 and pylint for linting & diagnostics.
🤖 LLM Feedback: Uses OpenAI’s API (or mock mode) to generate concise, actionable feedback.
🧩 Review Modes: Style, performance, readability, security.
🛠️ Suggested Fixes: Optionally generate improved Python code.
📂 Repo Support: Clone a GitHub repo and recursively analyze .py files.
🖥️ CLI Tool: Simple command-line interface for files or repos.
🔄 Mock Mode: Run tests and CLI without API credits (MOCK_LLM=true).
📊 Progress Bar: See repo analysis progress with tqdm.
📑 Output Formats: Save reviews as .txt or .md.
🚀 Quickstart


1. Clone & Install
git clone https://github.com/Jyrel-Mendoza/ai-code-reviewer.git
cd ai-code-reviewer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Setup Environment
Create a .env file in utils/ with your OpenAI key:
OPENAI_API_KEY=sk-yourkeyhere
# For testing without API usage:
MOCK_LLM=true

3. Run the CLI
Analyze a single file (style mode):
python main.py --file sample_test.py --mode style
Generate fixes (print to terminal):
python main.py --file sample_test.py --fix
Save fixed code to a new file:
python main.py --file sample_test.py --fix --output sample_test_fixed.py
Save review in Markdown:
python main.py --file sample_test.py --mode readability --save-format md --output review.md
Analyze an entire repo:
python main.py --repo https://github.com/psf/requests --mode performance --save-format txt --output repo_review.txt


🧪 Testing
All tests run in mock mode (no API calls).
Run:


pytest
📊 Example Output
Feedback
=== AI Feedback ===

• Variable name `badFunction` should follow snake_case.  
• Remove extra spaces in arithmetic expression.  
• Function `unused_code` is never called.  


Suggested Fix:
def add_numbers(x, y):
    return x + y