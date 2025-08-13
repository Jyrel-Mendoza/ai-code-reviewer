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

def pylint_parser_output(lines: List[str]) -> List[Dict]:
    issues = []

    for line in lines:
        if not line.strip():
            continue

        try:
            path, row, col, rest = line.split(":", 3)
            rest = rest.strip()

            # Split code from message
            code, message_with_symbol = rest.split(":", 1)
            message_with_symbol = message_with_symbol.strip()

            # Extract symbol if present (in parentheses at end)
            # NOTE, symbol means the type of error
            if "(" in message_with_symbol and message_with_symbol.endswith(")"):
                msg, symbol = message_with_symbol.rsplit("(", 1)
                message = msg.strip()
                symbol = symbol[:-1]  # remove closing ')'
            else:
                message = message_with_symbol
                symbol = ""

            issues.append({
                    "tool": "pylint",
                    "file": path,
                    "line": int(row),
                    "col": int(col),
                    "code": code.strip(),
                    "message": message,
                    "symbol": symbol
                })
        except ValueError:
            # Skip lines that don’t match expected format here!
            continue

    return issues   
