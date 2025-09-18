import argparse
import logging
from pathlib import Path

from analyzer.code_analyzer import CodeAnalyzer
from llm.openai_review import OpenAIReviewer
from utils.repo_utils import RepoUtils

from dotenv import load_dotenv

# Load environment variables from .env in project root
load_dotenv()

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    parser = argparse.ArgumentParser(description="AI Code Reviewer CLI")
    parser.add_argument("--file", type=str, help="Path to a Python file")
    parser.add_argument("--repo", type=str, help="GitHub repo URL")
    args = parser.parse_args()

    analyzer = CodeAnalyzer()
    reviewer = OpenAIReviewer()

    # Single file mode
    if args.file:
        path = Path(args.file)
        if not path.exists():
            logging.error(f"File {args.file} not found.")
            return
        logging.info(f"Analyzing {args.file}...")
        lint_results = analyzer.analyze_file(path)
        with open(path, "r") as f:
            code_content = f.read()

        #Testing
        print(code_content)
        print(lint_results)    

        
        feedback = reviewer.review(code_content, lint_results)
        print("\n=== AI Feedback ===\n")
        print(feedback)

    # Repo mode
    elif args.repo:
        logging.info(f"Cloning repo {args.repo}...")
        repo_files = RepoUtils.clone_and_list(args.repo)
        for file in repo_files:
            logging.info(f"Analyzing {file}...")
            lint_results = analyzer.analyze_file(file)
            with open(file, "r") as f:
                code_content = f.read()
            
            #Testing
            print(code_content)
            print(lint_results)
            feedback = reviewer.review(code_content, lint_results)
            print(f"\n=== Feedback for {file} ===\n")
            print(feedback)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()