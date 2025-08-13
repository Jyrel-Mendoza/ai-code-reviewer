from analyzer.static_tools import run_flake8, run_pylint
from analyzer.parser import flake8_parser_output, pylint_parser_output


if __name__ == "__main__":
    path_to_check = "analyzer/parser.py"

    flake8_raw_output = run_flake8(path_to_check)
    flake8_issues = flake8_parser_output(flake8_raw_output)

    print("Flake 8 issues: ")
    for issue in flake8_issues:
        print(issue)

    pylint_raw_output = run_pylint(path_to_check)
    pylint_issues = pylint_parser_output(pylint_raw_output)

    print("\nPylint Output: ")
    for issue in pylint_issues:
        print(issue)