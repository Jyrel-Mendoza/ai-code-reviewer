from typing import Dict, List


def flake8_parser_output(lines: List[str]) -> List[Dict]:
    """parses flake8 output into structured dictionaries"""

    issues = []
    for line in lines:
        if not line.strip():
            continue
        try:
            path, row, col, rest = line.split(":", 3)
            rest = rest.strip()
            code, message = rest.split(" ", 1)
            issues.append({
                "tool": "flake8",
                "file": path,
                "line": int(row),
                "col": int(col),
                "code": code,
                "message": message,

            })
        except ValueError:
            continue

    return issues
