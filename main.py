import argparse
import logging
from pathlib import Path

from analyzer.code_analyzer import CodeAnalyzer
from llm.openai_review import OpenAIReviewer
from utils.repo_utils import RepoUtils
from utils.output_writer import save_output   # NEW helper

from dotenv import load_dotenv
from tqdm import tqdm  # NEW for progress bars

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
    parser.add_argument("--mode", type=str,
                        choices=["style", "performance", "readability", "security"],
                        default="style",
                        help="Review mode: style, performance, readability, or security")
    parser.add_argument("--fix", action="store_true",
                        help="Also output suggested fixes for code")
    parser.add_argument("--output", type=str,
                        help="Optional file to save suggested fixes or reviews")
    parser.add_argument("--save-format", type=str,
                        choices=["txt", "md"],
                        help="Format for saving review output (txt or md)")
    args = parser.parse_args()

    reviewer = OpenAIReviewer()

    # Single file mode
    if args.file:
        path = Path(args.file)
        if not path.exists():
            logging.error(f"File {args.file} not found.")
            return
        logging.info(f"Analyzing {args.file}...")
        lint_results = CodeAnalyzer.analyze_file(path)

        with open(path, "r") as f:
            code_content = f.read()

        feedback = reviewer.review(code_content, lint_results, mode=args.mode)
        print("\n=== AI Feedback ===\n")
        print(feedback)

        # Save feedback if requested
        if args.output and args.save_format:
            save_output(feedback, Path(args.output), args.save_format)
            print(f"\n💾 Review saved to {args.output}")

        if args.fix:
            suggestion = reviewer.suggest_fixes(code_content, lint_results)
            print("\n=== Suggested Fix ===\n")
            print(suggestion)
            if args.output and not args.save_format:
                # If no format specified, just save raw fixed code
                with open(args.output, "w") as f:
                    f.write(suggestion)
                print(f"\n💾 Fixed code saved to {args.output}")

    # Repo mode
    elif args.repo:
        logging.info(f"Cloning repo {args.repo}...")
        repo_files = RepoUtils.clone_and_list(args.repo)

        all_feedback = []

        for file in tqdm(repo_files, desc="Analyzing files"):
            logging.info(f"Analyzing {file}...")
            lint_results = CodeAnalyzer.analyze_file(file)

            with open(file, "r") as f:
                code_content = f.read()

            feedback = reviewer.review(code_content, lint_results, mode=args.mode)
            print(f"\n=== Feedback for {file} ===\n")
            print(feedback)
            all_feedback.append(f"## {file}\n\n{feedback}\n")

            if args.fix:
                suggestion = reviewer.suggest_fixes(code_content, lint_results)
                print(f"\n=== Suggested Fix for {file} ===\n")
                print(suggestion)
                if args.output:
                    out_path = Path(args.output)
                    if out_path.is_dir():
                        fixed_file = out_path / Path(file).name
                    else:
                        fixed_file = out_path
                    with open(fixed_file, "w") as f:
                        f.write(suggestion)
                    print(f"\n💾 Fixed code saved to {fixed_file}")

        # Save combined repo feedback if requested
        if args.output and args.save_format and all_feedback:
            save_output("\n".join(all_feedback), Path(args.output), args.save_format)
            print(f"\n💾 Combined repo review saved to {args.output}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()