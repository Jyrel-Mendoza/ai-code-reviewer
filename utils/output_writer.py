from pathlib import Path

def save_output(content: str, output_path: Path, fmt: str = "txt"):
    if fmt == "md":
        header = "# AI Code Review\n\n"
        content = header + content
    output_path.write_text(content, encoding="utf-8")